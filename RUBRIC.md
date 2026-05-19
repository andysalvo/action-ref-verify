# Verdict Rubric v0.1

How the conformance harness grades vectors.

## Verdicts

| Verdict | Condition |
|---------|-----------|
| **PASS** | Canonical bytes produced by JCS (RFC 8785) match expected canonical form exactly, AND SHA-256 digest of those bytes matches the claimed `action_ref` exactly. |
| **FAIL** | Any byte-level divergence in canonical form, OR any divergence in SHA-256 digest. |
| **AMBIGUOUS** | Vector exposes a spec interpretation gap (e.g., the spec does not define behavior for the input). Logged as an issue, not graded PASS or FAIL. |

## Scope

This rubric applies to the **action-ref-v1-jcs-sha256** profile only:

- **In scope:** JCS canonicalization (RFC 8785, lexicographic key ordering, no whitespace) + SHA-256 hash derivation over canonical bytes
- **Out of scope:** Ed25519 signatures, two-receipt models, payment hash verification, on-chain settlement checks

Ed25519 signature verification is tracked as a separate profile (`ed25519-two-receipt`). The two profiles are independently testable. A vector can pass hash verification and fail signature verification, or vice versa.

## What gets hashed

The verifier extracts exactly four fields from the preimage object: `action_type`, `agent_id`, `scope`, `timestamp`. Extra fields are ignored. The extracted object is canonicalized via JCS and hashed with SHA-256.

## Timestamp format

RFC 3339 UTC with 3-digit millisecond precision (e.g., `2025-05-18T11:40:31.000Z`). JCS treats timestamps as opaque strings. `2025-05-18T11:40:31Z` and `2025-05-18T11:40:31.000Z` produce different hashes.

## All implementations graded equally

The same rubric applies to all implementations, including the harness itself. argentum-core, nobulex, and action-ref-verify are all graded by the same fixtures under the same rules.

## Disputes

See [CONFORMANCE_INTAKE.md](CONFORMANCE_INTAKE.md) for the dispute process.
