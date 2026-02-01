# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this project, please report it responsibly.

**Do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please email security concerns to: [security@your-org.com]

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes

We will acknowledge receipt within 48 hours and provide a detailed response within 7 days.

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Security Considerations

### API Keys

- Never commit API keys to the repository
- Use environment variables for all secrets
- Rotate keys if accidentally exposed

### Generated Content

This software generates draft procedural content. All output includes disclaimers and is intended for review by qualified professionals only.

### Data Storage

- Feedback data is stored locally by default
- No sensitive data should be included in feedback submissions
- Review data retention policies for your deployment
