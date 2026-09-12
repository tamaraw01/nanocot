# NanoCoT: Fast Reasoning & Response Proxy for LLM Routers

NanoCoT is a Python proxy middleware designed for LLM routing setups. It brings fast reasoning capabilities to smaller models like Claude 3.5 Haiku, GPT-4o-mini, and Qwen, giving them accuracy closer to flagship models without the latency penalty of long Chain-of-Thought (CoT) traces.

When using router endpoints that rotate across different model tiers (such as round-robin setups), smaller models can struggle with complex multi-step reasoning. NanoCoT fixes this by dynamically injecting a low-overhead reasoning budget for complex prompts while stripping the reasoning tokens before sending output back to your app.

---

## Core Capabilities

- **Dynamic Complexity Classifier:** Scans incoming prompts to separate simple tasks from complex ones. Basic queries pass through directly without reasoning delays.
- **Token-Budgeted Micro-CoT:** For complex tasks, NanoCoT injects a concise system directive (`<nanocot_think>`) capped at an 80-word budget. This gives smaller models structured reasoning without long generation times.
- **Physical Response Sanitizer:** Operates on both standard and streaming responses to strip out thinking tags at the proxy layer. Your app receives only the clean, final answer.
- **OpenAI-Compatible Endpoint:** Acts as a transparent proxy for existing apps (Hermes, Claude Code, custom frontend scripts). Just swap your base URL.

---

## Architecture Overview

```
[Incoming Request]
        │
        ▼
[Complexity Classifier] ─── (Simple Prompt) ───► [Direct Forward to Router]
        │                                                     │
 (Complex Prompt)                                             │
        │                                                     │
        ▼                                                     │
[Micro-CoT Injector]                                          │
        │                                                     │
        ▼                                                     │
[Upstream Provider / Router] ◄────────────────────────────────┘
        │
        ▼
[Physical Response Sanitizer] (Strips <nanocot_think> from Stream/JSON)
        │
        ▼
[Clean Response to Client]
```

---

## Installation

### Prerequisites

- Python 3.11+

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/tamaraw01/nanocot.git
   cd nanocot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration & Usage

Set your target upstream provider or router endpoint:

```bash
export UPSTREAM_BASE_URL="http://127.0.0.1:20128/v1"
export UPSTREAM_API_KEY="sk-your-key-here"
```

Start the proxy server:

```bash
python3 server.py
```

By default, the proxy listens on `http://0.0.0.0:8888`.

### Integrating with Hermes Agent

Point Hermes to the proxy endpoint:

```bash
hermes config set providers.openai.base_url "http://127.0.0.1:8888/v1"
hermes config set providers.openai.api_key "sk-dummy"
```

---

## Verification & Testing

Run the test suite to verify non-streaming and streaming sanitization:

```bash
python3 test_engine.py
```

Expected output:
```text
✓ ComplexityClassifier test passed.
✓ MicroCoTInjector test passed.
✓ PhysicalResponseSanitizer Non-Streaming test passed.
✓ PhysicalResponseSanitizer Streaming test passed.

ALL NANOCOT ENGINE TESTS PASSED GREEN!
```

---

## Model Support Matrix

| Category | Representative Models | Performance Note |
|---|---|---|
| **Tier A (High Parity)** | Claude 3.5 Haiku, GPT-4o-mini, Qwen 2.5 72B, Llama 3.3 70B | Excellent accuracy gains with Micro-CoT; low latency impact. |
| **Tier B (Base Utility)** | Models <3B parameters | Improved structure, but overall capacity remains bound by model parameter scale. |

---

## License

Distributed under the MIT License. See `LICENSE` for details.
