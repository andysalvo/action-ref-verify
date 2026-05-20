# action-ref-verify

Conformance verifier for x402 post-settlement `action_ref` fields.

Re-derives `action_ref` using **JCS (RFC 8785) + SHA-256** and verifies it matches the claimed hash. Context: [x402-foundation/x402#2332](https://github.com/x402-foundation/x402/issues/2332).

## Usage

```bash
npm install
node verify.mjs vectors/0001-giskard-baseline.json
```

Or pipe:
```bash
echo '{"action_ref":"fdd7f8...","preimage":{"agent_id":"x","action_type":"y","scope":"z","timestamp":"2025-05-18T11:40:31.000Z"}}' | node verify.mjs
```

## Hosted API

Submit receipts and get conformance verdicts without running the CLI:

```bash
curl -X POST https://verify.crestsystems.ai/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"action_ref":"<sha256>","preimage":{"action_type":"...","agent_id":"...","scope":"...","timestamp":"..."}}'
```

Returns a signed verdict with a public permalink at `verify.crestsystems.ai/v1/verdict/:id`.

## Canonical derivation

```
action_ref = SHA-256(JCS(preimage_object))
```

Where JCS is [JSON Canonicalization Scheme (RFC 8785)](https://www.rfc-editor.org/rfc/rfc8785):
- Keys sorted lexicographically (alphabetical for ASCII)
- No whitespace
- Field names are opaque bytes (load-bearing in the digest)

Two timestamp encodings are supported:
- `timestamp_ms` (integer, epoch milliseconds) -- per the original #2332 preimage spec
- `timestamp` (string, RFC 3339 UTC) -- legacy encoding from early verifier versions

These produce different digests. The field name is part of the JCS canonical output. See vector 0009 for a worked proof.

## Fixture format

```json
{
  "action_ref": "<SHA-256 hex>",
  "preimage": {
    "action_type": "sanctions_screen",
    "agent_id": "did:web:agent-7.example.com",
    "scope": "counterparty-due-diligence",
    "timestamp_ms": 1747728000000
  },
  "payment_hash": "<Base tx hash (optional)>",
  "spec": "action-ref-v1-jcs-sha256"
}
```

## What it checks

1. Re-derives `action_ref` as `SHA-256(JCS(preimage))` and compares to claimed hash
2. Verifies `payment_hash` is present (if provided)
3. Verifies `spec` field is declared

Returns `PASS` or `FAIL` with detailed check results.

## Conformance vectors

| Vector | Implementation | Source | Status |
|--------|---------------|--------|--------|
| `0001-giskard-baseline` | argentum-core | [#2332](https://github.com/x402-foundation/x402/issues/2332) | PASS |
| `0002-ms-precision-trap` | crest-adversarial | v0.2.0 | FAIL (by design) |
| `0003-trailing-whitespace` | crest-adversarial | v0.2.0 | FAIL (by design) |
| `0004-extra-field-ignored` | crest-adversarial | v0.2.0 | PASS |
| `0005-key-order-resilience` | crest-adversarial | v0.2.0 | PASS |
| `0006-rfc8785-negative-zero` | rfc8785-appendix-b | v0.2.0 | PASS |
| `0007-rfc8785-key-sorting-stress` | rfc8785-appendix-b | v0.2.0 | PASS |
| `0008-x402-2357-shared-fixture` | crest-interop | [#2357](https://github.com/x402-foundation/x402/issues/2357) | PASS |
| `0009-field-name-load-bearing` | crest-adversarial | v0.3.0 | FAIL (by design) |

See [CONFORMANCE_INTAKE.md](CONFORMANCE_INTAKE.md) for submission format and publication policy.

## Built by

[Crest Deployment Systems](https://crestsystems.ai) -- deploying scalable intelligence.
