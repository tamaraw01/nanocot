# Changelog

All notable changes to this project are documented here.

## [1.0.0] 2026-09-13

### Initial Release

- **Dynamic Complexity Classifier**: Evaluates request complexity. Routes simple queries directly, complex queries to reasoning pipeline.
- **Micro-CoT Injector**: Adds a reasoning budget (80 words max) to system prompt for complex tasks only.
- **Physical Response Sanitizer**: Removes reasoning tags from responses before sending to client.
- **OpenAI-Compatible Proxy**: Full `/v1/chat/completions` and `/v1/models` support. Works with any OpenAI-compatible client.
- **Test Suite**: Comprehensive tests for all core components.
- **Documentation**: README, contributing guide, security policy, code of conduct.

### Supported Models

Tier A: Claude 3.5 Haiku, GPT-4o-mini, Qwen 2.5 72B, Llama 3.3 70B (90-95% parity with larger models)

Tier B: Models <3B parameters (reasoning structure improves, capacity-limited by size)

### Known Limitations

- Reasoning budget (80 words) is fixed. Customization coming in v1.1.
- No telemetry or usage tracking. All processing is local.
