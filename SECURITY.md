# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, email the maintainers with:
- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Suggested fix (if available)

Do not open a public issue for security vulnerabilities.

## Security Best Practices

When deploying NanoCoT:

1. **API Key Management**: Never commit `.env` files. Use environment variables or a secrets manager.
2. **Upstream Authentication**: Verify your router's API key is strong and rotated regularly.
3. **Network Isolation**: In production, run NanoCoT on a private network or behind a firewall.
4. **Proxy Updates**: Keep the proxy up to date for any security patches.

## Supported Versions

Only the latest version receives security updates. Upgrade frequently.

## Data privacy and upstream requests

NanoCoT forwards chat-completion request bodies, including messages and any injected reasoning directive, to `UPSTREAM_BASE_URL`. Responses return through the proxy, which sanitizes the first choice's text before returning a non-streaming response or sanitizes text chunks for streaming responses. Processing is not confined to the proxy: the configured upstream receives the request data.

For chat completions, the proxy forwards the client's `Authorization` header when present. Otherwise, it sends `UPSTREAM_API_KEY`. Model-list requests use `UPSTREAM_API_KEY`. Choose a trusted upstream and check its retention and logging policies before sending sensitive data.

The server does not implement incoming API-key validation. A client that can reach the proxy can submit requests using the configured upstream key when it omits its own authorization header. Keep the proxy on a restricted network or place it behind an authenticated gateway. CORS settings do not provide access control.

These behaviors are implemented in [server.py](server.py). Reasoning-tag removal is response formatting, not a guarantee that sensitive information has been removed.
