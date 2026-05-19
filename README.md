# action-ref-verify

Conformance verifier for x402 post-settlement `action_ref` fields.

Re-derives `action_ref` using **JCS (RFC 8785) + SHA-256** and verifies it matches the claimed hash. Context: [x402-foundation/x402#2332](https://github.com/x402-foundation/x402/issues/2332).

## Usage

```bash
npm install
node verify.mjs fixtures/nexus-canonical.json
```

Or pipe:
```bash
echo '{"action_ref":"fdd7f8...","preimage":{"agent_id":"x","action_type":"y","scope":"z","timestamp":"2025-05-18T11:40:31.000Z"}}' | node verify.mjs
```

## Canonical derivation

```
action_ref = SHA-256(JCS(preimage_object))
```

Where JCS is [JSON Canonicalization Scheme (RFC 8785)](https://www.rfc-editor.org/rfc/rfc8785):
- Keys sorted lexicographically (alphabetical for ASCII)
- No whitespace
- Timestamps are RFC 3339 UTC with 3-digit ms precision

## Fixture format

```json
{
  "action_ref": "<SHA-256 hex>",
  "preimage": {
    "action_type": "oracle.signal",
    "agent_id": "nexus-agent-xa12.onrender.com",
    "scope": "BTC",
    "timestamp": "2025-05-18T11:40:31.000Z"
  },
  "payment_hash": "<Base tx hash (optional)>",
  "spec": "x402-action-ref-jcs-sha256"
}
```

## What it checks

1. Re-derives `action_ref` as `SHA-256(JCS(preimage))` and compares to claimed hash
2. Verifies `payment_hash` is present (if provided)
3. Verifies `spec` field is declared

Returns `PASS` or `FAIL` with detailed check results.

## Conformance fixtures

| Fixture | Source | Status |
|---------|--------|--------|
| `fixtures/nexus-canonical.json` | [argentum-core@77a10ff](https://github.com/giskard09/argentum-core/blob/main/docs/spec/action-ref.md) | PASS |

## Built by

[Crest Deployment Systems](https://crestsystems.ai) -- deploying scalable intelligence.
