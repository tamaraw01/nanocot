# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability, email security@tamaraw01.dev with:
- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Suggested fix (if available)

Please do not open a public issue for security vulnerabilities.

## Security Best Practices

When deploying NanoCoT:

1. **API Key Management** — Never commit `.env` files. Use environment variables or a secrets manager.
2. **Upstream Authentication** — Verify your router's API key is strong and rotated regularly.
3. **Network Isolation** — In production, run NanoCoT on a private network or behind a firewall.
4. **Proxy Updates** — Keep the proxy up to date for any security patches.

## Supported Versions

Only the latest version receives security updates. Upgrade frequently.

## Data Privacy

NanoCoT does not log, store, or transmit request/response data. All processing is local to the proxy instance.
