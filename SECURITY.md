# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this verifier, please report it responsibly.

**Email:** andysalvo26@gmail.com

**Do not** open a public issue for security vulnerabilities.

We will acknowledge receipt within 48 hours and provide a timeline for resolution.

## Scope

This policy covers:
- The `verify.mjs` verifier logic
- The vendored `canonicalize` implementation
- The vector intake and report generation process
- Any hosted API endpoint that mirrors this CLI

## Dependency Policy

The JCS canonicalization function (`vendor/canonicalize.mjs`) is vendored from `canonicalize@3.0.0` with a pinned SHA-256 integrity hash. We do not use the npm package at runtime. Changes to the vendored source require a signed commit and review.

## Disclosure Timeline

- **Day 0:** Report received, acknowledgment sent
- **Day 7:** Assessment complete, fix timeline communicated
- **Day 30:** Fix released or mitigation documented
- **Day 90:** Public disclosure (coordinated with reporter)
