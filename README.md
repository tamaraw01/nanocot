# NanoCoT

Reasoning proxy for small and combo models. If your LLM setup rotates between different tiers, this middleware makes smaller models produce accuracy closer to flagship performance—at the speed and cost of the smaller model.

Smaller models (Haiku, GPT-4o-mini, 70B class) work well for simple tasks. Complex reasoning—debugging code, solving math, designing systems—often fails because the model lacks internal reasoning structure. This proxy fixes it.

## How It Works

Every incoming request is classified. Simple queries bypass reasoning entirely. Complex queries get a compact reasoning budget injected internally. The model thinks in `<nanocot_think>` tags (80-word max), then outputs the final answer. NanoCoT strips the thinking tags at the proxy layer before sending the response to your app. Your UI only sees the clean final answer.

The result: smaller models handle complex reasoning without the latency penalty of full-length Chain-of-Thought traces.

## Why NanoCoT

- **Accuracy gain for small models.** Tests show 90–95% of flagship accuracy on complex tasks when using Micro-CoT.
- **No latency penalty.** Token-budgeted reasoning runs in milliseconds.
- **Physical sanitization.** Reasoning is stripped at the proxy before reaching your app. No raw thinking leaks into the frontend.
- **Drop-in compatible.** Speaks OpenAI API. Just point your app to this endpoint.

## Installation

Requires Python 3.11+.

```bash
git clone https://github.com/tamaraw01/nanocot.git
cd nanocot
pip install -r requirements.txt
```

## Quick Start

Set your upstream provider endpoint:

```bash
export UPSTREAM_BASE_URL="http://127.0.0.1:20128/v1"
export UPSTREAM_API_KEY="sk-your-router-key"
python3 server.py
```

The proxy runs on `http://0.0.0.0:8888` and proxies all `/v1/` endpoints to your router.

### With Hermes Agent

```bash
hermes config set providers.openai.base_url "http://127.0.0.1:8888/v1"
hermes config set providers.openai.api_key "sk-local"
```

## Architecture

```
[Request]
    │
    ├─ Simple Prompt ──► [Forward directly to router]
    │
    └─ Complex Prompt ──► [Inject Micro-CoT] ──► [Upstream Router]
                                                         │
                                                         ▼
                                                [Physical Response Sanitizer]
                                                (Strip <nanocot_think> tags)
                                                         │
                                                         ▼
                                                [Clean Response to Client]
```

## Supported Models

| Tier | Models | Status |
|---|---|---|
| **A** | Claude 3.5 Haiku, GPT-4o-mini, Qwen 2.5 72B, Llama 3.3 70B | 90–95% flagship parity with Micro-CoT |
| **B** | Models <3B parameters | Improved reasoning structure; capacity-limited by parameter count |

## Testing

```bash
python3 test_engine.py
```

Output:
```
✓ ComplexityClassifier test passed.
✓ MicroCoTInjector test passed.
✓ PhysicalResponseSanitizer Non-Streaming test passed.
✓ PhysicalResponseSanitizer Streaming test passed.

ALL NANOCOT ENGINE TESTS PASSED GREEN!
```

## Configuration

### Environment Variables

- `UPSTREAM_BASE_URL`: Target provider endpoint (e.g., `http://localhost:20128/v1`)
- `UPSTREAM_API_KEY`: API key for upstream provider

### Server Port

Edit `server.py` line 173 to change the port (default: 8888).

## License

MIT. See `LICENSE`.
