# NanoCoT Changelog

All notable changes to this project are documented here.

## [1.0.0] - 2026-09-13

### Initial Release

- **Dynamic Complexity Classifier** — Evaluates prompt complexity; routes simple queries directly, complex queries to Micro-CoT pipeline.
- **Micro-CoT Injector** — Injects compact reasoning budget (80 words max) into system directive for complex tasks.
- **Physical Response Sanitizer** — Strips reasoning tags from both standard and streaming responses before client delivery.
- **OpenAI-Compatible Proxy** — Full `/v1/chat/completions` and `/v1/models` support; works with any OpenAI-compatible client.
- **Test Suite** — Comprehensive tests for all core components (non-streaming, streaming, sanitization).
- **Documentation** — README, contributing guide, architecture overview.

### Supported Models

- Tier A: Claude 3.5 Haiku, GPT-4o-mini, Qwen 2.5 72B, Llama 3.3 70B (90–95% flagship parity)
- Tier B: Models <3B parameters (reasoning structure improved; capacity-limited)

### Known Limitations

- Reasoning budget (80 words) is fixed; user customization coming in v1.1.
- No telemetry or usage tracking; all processing is local.
