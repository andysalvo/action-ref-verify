# Verification Scope

## What this harness verifies

**Profile: action-ref-v1-jcs-sha256**

Given a preimage object containing `action_type`, `agent_id`, `scope`, and `timestamp`:

1. Canonicalize the object using JCS (RFC 8785): lexicographic key ordering, no whitespace, UTF-8
2. Compute SHA-256 over the canonical byte sequence
3. Compare the resulting digest to the claimed `action_ref`

That is the entire scope of verification for this profile.

## What this harness does NOT verify

- Ed25519 or other digital signatures (separate profile: `ed25519-two-receipt`)
- Payment hash validity or on-chain settlement
- Agent identity or reputation
- Service delivery or quality
- Facilitator behavior
- Compliance with any regulation

## Why the scope is narrow

A conformance harness is only useful if its verdicts are deterministic and reproducible. By limiting scope to canonicalization + hashing, any implementation in any language can independently reproduce every verdict from the published fixtures.

Broader verification (signatures, settlement, delivery) requires additional trust assumptions and is tracked under separate profiles with their own rubrics.
