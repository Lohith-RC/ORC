# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.1.x   | :white_check_mark: |
| 2.0.x   | :white_check_mark: |
| < 2.0   | :x:                |

## Reporting a Vulnerability

The OSCC AI team takes the security and integrity of patient diagnostic software seriously. If you discover a security vulnerability or medical privacy leak, please report it promptly.

### How to Report

- **Email**: lohith.developer@gmail.com (or repository maintainers)
- Please include:
  1. Description of the vulnerability and attack vector
  2. Reproduction steps or Proof of Concept (PoC)
  3. Affected component(s) (e.g., API endpoint, authentication middleware, CORS headers)
  4. Suggested remediation if available

### Security Architecture Highlights

1. **Zero Wildcard CORS in Production**: Origins are restricted to an explicit environment-controlled whitelist (`CORS_ORIGINS`).
2. **Defensive Cryptography**: Passwords hashed with PBKDF2-HMAC-SHA256 (390,000 rounds) + unique salt; JWT secret keys strictly validated at startup.
3. **Medical Privacy (PHI)**:
   - Patient metadata strictly submitted via multipart body (zero PHI in URL query parameters).
   - `Cache-Control: no-store, no-cache, max-age=0` enforced on all diagnostic and patient history endpoints.
4. **Header Lockdown**:
   - `Content-Security-Policy: default-src 'self'; frame-ancestors 'none';`
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY`
   - `X-XSS-Protection: 1; mode=block`
   - `Permissions-Policy: camera=(self), microphone=(), geolocation=()`
   - `Strict-Transport-Security` enabled over HTTPS
5. **Streaming Chunk Protection**: Upload endpoints enforce 64KB chunk-based early exit guards against denial-of-service and memory exhaustion.
