# action-ref-verify

Draft conformance verifier for x402 settlement receipt `action_ref` fields.

Re-derives `action_ref` from preimage fields and checks it matches the claimed hash. Context: [x402-foundation/x402#2332](https://github.com/x402-foundation/x402/issues/2332).

## Usage

```bash
node verify.mjs fixture.json
```

Or pipe:
```bash
echo '{"action_ref":"abc...","preimage":{"agent_id":"x","action_type":"y","scope":"z","ts":"123"}}' | node verify.mjs
```

## Fixture format

```json
{
  "action_ref": "<SHA-256 hex>",
  "payment_hash": "<Base tx hash>",
  "preimage": {
    "agent_id": "service.example.com",
    "action_type": "oracle.signal",
    "scope": "BTC",
    "ts": "1747568431"
  },
  "spec": "argentum-core/action-ref-v1"
}
```

## What it checks

1. Re-derives `action_ref` as `SHA-256(agent_id:action_type:scope:ts)` and compares to claimed hash
2. Verifies `payment_hash` is present
3. Verifies `spec` field is declared

Returns `PASS` or `FAIL` with detailed check results.

## Status

Draft. Canonical encoding (delimiter, casing, field order) needs alignment with the argentum-core spec.

## Built by

[Crest Deployment Systems](https://crestsystems.ai) -- deploying scalable intelligence.
