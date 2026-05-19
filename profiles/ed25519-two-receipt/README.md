# Profile: ed25519-two-receipt

Ed25519 signed two-receipt model for post-settlement accountability.

## Status

**Pending spec.** This profile will be implemented when Nobulex or other implementations provide:

- Spec document describing the two-receipt model
- Reference vectors with signed payloads
- Public keys for signature verification
- Exact byte-level description of what is signed

## Architecture

This profile is orthogonal to `action-ref-v1-jcs-sha256`. The JCS+SHA-256 profile produces the canonical `action_ref`; the Ed25519 two-receipt profile describes how receipts containing `action_ref` values are signed and verified.

They are composable, not competing.
