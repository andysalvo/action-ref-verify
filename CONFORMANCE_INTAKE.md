# Conformance Vector Intake

This harness verifies `action_ref` derivations against [x402 post-settlement accountability](https://github.com/x402-foundation/x402/issues/2332).

## Submitting a vector

Open an issue or PR with a JSON file in `vectors/` following this schema:

```json
{
  "name": "short-descriptive-name",
  "implementation": "implementation-name",
  "version": "commit-hash-or-semver",
  "spec": "action-ref-v1-jcs-sha256",
  "expected_result": "PASS",
  "action_ref": "<expected SHA-256 hex digest>",
  "preimage": {
    "action_type": "...",
    "agent_id": "...",
    "scope": "...",
    "timestamp": "RFC 3339 UTC, 3-digit ms precision"
  },
  "notes": "optional context"
}
```

### Required fields

| Field | Description |
|-------|-------------|
| `name` | Short slug for the vector |
| `implementation` | Name of the submitting implementation |
| `version` | Pinned commit hash or version |
| `spec` | Protocol profile being tested |
| `expected_result` | `PASS` or `FAIL` |
| `action_ref` | The claimed SHA-256 hex digest |
| `preimage` | The input object with all four fields |

### Supported profiles

| Profile | Method | Status |
|---------|--------|--------|
| `action-ref-v1-jcs-sha256` | JCS (RFC 8785) + SHA-256 | Active |
| `ed25519-two-receipt` | Ed25519 signed receipts | Pending spec |

New profiles are added when spec documents and at least one reference vector are provided.

## Publication policy

- Submitted vectors are public by default.
- Every published result includes: harness version, fixture hash, canonical bytes, computed action_ref, expected action_ref, and pass/fail verdict.
- Failing vectors are published with the same rigor as passing vectors.
- Ambiguous specimens (underspecified input, missing fields) are marked `INCONCLUSIVE`.
- If a vector must remain private, state this explicitly before submission. Private vectors require separate handling terms.

## Report format

Each run produces:

```
VECTOR: 0001-giskard-baseline
RESULT: PASS
HARNESS: action-ref-verify@ec7201a
SPEC: action-ref-v1-jcs-sha256
CANONICAL: {"action_type":"oracle.signal","agent_id":"nexus-agent-xa12.onrender.com","scope":"BTC","timestamp":"2025-05-18T11:40:31.000Z"}
EXPECTED: fdd7f810499f06be24355ca8e2bfb8c4b965cc80c838f41fa074683443d89f5a
COMPUTED: fdd7f810499f06be24355ca8e2bfb8c4b965cc80c838f41fa074683443d89f5a
DIFF: none
```

On failure, the `DIFF` field shows the exact byte-level divergence.

## What this harness does not do

- It does not certify implementations.
- It does not warrant spec correctness.
- It verifies against the spec as written at the pinned version.
- Results identify harness version and spec version explicitly.

## Maintained by

[Crest Deployment Systems](https://crestsystems.ai) -- deploying scalable intelligence.
