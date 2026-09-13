# NanoCoT

[![GitHub](https://img.shields.io/badge/GitHub-tamaraw01%2Fnanocot-blue?style=flat-square&logo=github)](https://github.com/tamaraw01/nanocot)
[![License MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?style=flat-square)](https://www.python.org/downloads/)
[![Tests Passing](https://img.shields.io/badge/Tests-Passing-green?style=flat-square)](test_engine.py)

> A reasoning proxy that makes small language models (Claude 3.5 Haiku, GPT-4o-mini, 70B class) produce results on par with larger models, without slowdown.

## The Situation

When you rotate between different model sizes, smaller models often struggle with complex reasoning. They lack the internal structure for debugging code, solving math problems, or designing systems across multiple steps.

Common workarounds use long Chain-of-Thought traces. This fixes accuracy but creates a new problem: your application waits for hundreds of reasoning tokens before the final answer arrives.

## How NanoCoT Works

NanoCoT sits at the proxy layer. It evaluates each request for complexity in microseconds. Complex requests get a strict 80-word reasoning budget injected into the system prompt. The model reasons inside `<nanocot_think>` tags, then outputs the answer. NanoCoT strips the thinking tags before sending the response to your application.

**Result:** Smaller models handle complex reasoning in milliseconds, with accuracy in the 90-95% range compared to larger models.

---

## What You Get

- **Smart Routing** – Simple queries skip reasoning entirely. Complex queries get a reasoning budget.
- **Fast Reasoning** – Capped at 80 words. No rambling, no delays.
- **Clean Output** – Reasoning is removed at the proxy layer. Your UI only sees the final answer.
- **Standard Interface** – Uses OpenAI API format. Works with any compatible client.
- **Minimal Overhead** – Token-budgeted reasoning adds no noticeable latency.

---

## Getting Started

### Installation

```bash
git clone https://github.com/tamaraw01/nanocot.git
cd nanocot
pip install -r requirements.txt
```

### Launch

```bash
export UPSTREAM_BASE_URL="http://your-router:port/v1"
export UPSTREAM_API_KEY="sk-your-key"
python3 run.py
```

The proxy listens on `http://0.0.0.0:8888`.

### Integration with Any OpenAI-Compatible Client

Point your client to the proxy endpoint:

```bash
# With curl
curl http://localhost:8888/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"haiku","messages":[{"role":"user","content":"Your prompt"}]}'

# With Python
import httpx
client = httpx.Client()
response = client.post("http://localhost:8888/v1/chat/completions", json=...)
```

---

## How It Works

```
Request
  ├─ Simple Prompt ────► Forward directly to upstream
  │
  └─ Complex Prompt ────► Add reasoning budget ────► Forward to upstream
                                                         │
                                                         ▼
                                             Strip reasoning tags
                                                         │
                                                         ▼
                                             Clean response to client
```

---

## Model Compatibility

| Tier | Models | Result |
|---|---|---|
| **A** | Claude 3.5 Haiku, GPT-4o-mini, Qwen 2.5 72B, Llama 3.3 70B | 90-95% parity with larger models |
| **B** | Models <3B parameters | Reasoning improves, but limited by model size |

---

## Testing

```bash
python3 test_engine.py
```

Expected output:
```
✓ ComplexityClassifier test passed.
✓ MicroCoTInjector test passed.
✓ PhysicalResponseSanitizer Non-Streaming test passed.
✓ PhysicalResponseSanitizer Streaming test passed.

ALL NANOCOT ENGINE TESTS PASSED GREEN!
```

---

## Usage Examples

### Direct HTTP Request

```python
import httpx
import json

client = httpx.Client()
response = client.post(
    "http://localhost:8888/v1/chat/completions",
    json={
        "model": "haiku",
        "messages": [
            {"role": "user", "content": "Write a Python async database pool."}
        ],
        "stream": False
    }
)

result = response.json()
print(result["choices"][0]["message"]["content"])
# Returns clean implementation without reasoning artifacts
```

### Streaming Responses

```python
response = client.post(
    "http://localhost:8888/v1/chat/completions",
    json={
        "model": "haiku",
        "messages": [{"role": "user", "content": "..."}],
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line.startswith("data: "):
        data = json.loads(line[6:])
        # Content is already clean (no reasoning tags)
        print(data)
```

See `example.py` for a complete working example.

---

## Configuration

### Environment Variables

- `UPSTREAM_BASE_URL` – Your router endpoint, e.g. `http://localhost:20128/v1`
- `UPSTREAM_API_KEY` – API key for your upstream provider

### Server Port

Edit `run.py` line 33 to change the port (default: 8888).

---

## Documentation

- [CONTRIBUTING](CONTRIBUTING.md) – How to contribute
- [CHANGELOG](CHANGELOG.md) – Version history
- [SECURITY](SECURITY.md) – Security practices
- [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md) – Community guidelines

---

## License

MIT. See [LICENSE](LICENSE).

---

## Questions or Issues?

Open an [issue](https://github.com/tamaraw01/nanocot/issues) on GitHub.

Want to help? See [CONTRIBUTING](CONTRIBUTING.md).
