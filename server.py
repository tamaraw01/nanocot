"""
NanoCoT OpenAI-Compatible Proxy Server
Routes requests to an upstream provider (OpenRouter, OpenAI, or any router) while applying
Dynamic Micro-CoT and Physical Response Sanitization.
"""

import os
import json
import httpx
from typing import List, Dict, Any, AsyncGenerator
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core import ComplexityClassifier, MicroCoTInjector, PhysicalResponseSanitizer

app = FastAPI(
    title="NanoCoT Proxy Engine",
    description="Ultra-fast Token-Budgeted Reasoning & Physical Response Sanitizer Proxy",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = ComplexityClassifier()
injector = MicroCoTInjector()
sanitizer = PhysicalResponseSanitizer()

# Target upstream settings (defaults to any OpenAI-compatible router endpoint)
UPSTREAM_BASE_URL = os.getenv("UPSTREAM_BASE_URL", "http://localhost:20128/v1").rstrip("/")
UPSTREAM_API_KEY = os.getenv("UPSTREAM_API_KEY", "sk-dummy")


@app.get("/")
async def health_check():
    return {
        "status": "online",
        "engine": "NanoCoT Dynamic Reasoning Proxy",
        "version": "1.0.0"
    }


@app.get("/v1/models")
async def list_models():
    """Proxy models endpoint."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.get(
                f"{UPSTREAM_BASE_URL}/models",
                headers={"Authorization": f"Bearer {UPSTREAM_API_KEY}"}
            )
            return JSONResponse(status_code=resp.status_code, content=resp.json())
        except Exception as e:
            return JSONResponse(
                status_code=200,
                content={
                    "object": "list",
                    "data": [{"id": "nanocot-combo", "object": "model", "owned_by": "nanocot"}]
                }
            )


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    messages = body.get("messages", [])
    stream = body.get("stream", False)
    
    # 1. Complexity Classification
    is_complex = classifier.classify(messages)
    
    # 2. Inject Micro-CoT if complex
    if is_complex:
        messages = injector.inject(messages)
        body["messages"] = messages

    # Headers for upstream API
    headers = {
        "Content-Type": "application/json",
        "Authorization": request.headers.get("Authorization", f"Bearer {UPSTREAM_API_KEY}")
    }

    client = httpx.AsyncClient(timeout=120.0)

    if not stream:
        # Non-streaming handling
        try:
            resp = await client.post(
                f"{UPSTREAM_BASE_URL}/chat/completions",
                json=body,
                headers=headers
            )
            await client.aclose()
            
            if resp.status_code != 200:
                return JSONResponse(status_code=resp.status_code, content=resp.json())

            data = resp.json()
            # 3. Sanitize Non-Streaming Output physically
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                if "message" in choice and "content" in choice["message"]:
                    raw_content = choice["message"]["content"] or ""
                    choice["message"]["content"] = sanitizer.sanitize_text(raw_content)

            return JSONResponse(content=data)

        except Exception as e:
            await client.aclose()
            raise HTTPException(status_code=500, detail=f"Upstream Proxy Error: {str(e)}")

    else:
        # Streaming handling
        req = client.build_request(
            "POST",
            f"{UPSTREAM_BASE_URL}/chat/completions",
            json=body,
            headers=headers
        )

        async def sse_generator():
            try:
                upstream_resp = await client.send(req, stream=True)
                
                async def raw_chunk_gen():
                    async for line in upstream_resp.aiter_lines():
                        if not line:
                            continue
                        if line.startswith("data: "):
                            data_str = line[6:].strip()
                            if data_str == "[DONE]":
                                break
                            try:
                                chunk_json = json.loads(data_str)
                                choices = chunk_json.get("choices", [])
                                if choices and "delta" in choices[0]:
                                    delta = choices[0]["delta"]
                                    if "content" in delta and delta["content"]:
                                        yield delta["content"]
                            except Exception:
                                pass

                # Pass through Physical Response Sanitizer state machine
                async for clean_chunk in sanitizer.sanitize_stream(raw_chunk_gen()):
                    chunk_payload = {
                        "id": "nanocot-stream",
                        "object": "chat.completion.chunk",
                        "choices": [{"delta": {"content": clean_chunk}, "finish_reason": None}]
                    }
                    yield f"data: {json.dumps(chunk_payload)}\n\n"
                
                yield "data: [DONE]\n\n"

            finally:
                await upstream_resp.aclose()
                await client.aclose()

        return StreamingResponse(sse_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8888)
