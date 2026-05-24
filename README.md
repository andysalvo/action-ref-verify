# action-ref-verify

Conformance verifier for x402 `action_ref` work-receipt binding.

Re-derives `action_ref` using **JCS (RFC 8785) + SHA-256** and verifies it matches the claimed hash. Context: [x402-foundation/x402#2332](https://github.com/x402-foundation/x402/issues/2332), [PR #2398](https://github.com/x402-foundation/x402/pull/2398).

## Usage

```bash
# Node.js
npm install
node verify.mjs vectors/0001-giskard-baseline.json
node run-all.mjs

# Python
pip install rfc8785
python3 runner_python.py
```

## Hosted API

```bash
curl -X POST https://verify.crestsystems.ai/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"action_ref":"<sha256>","preimage":{"action_type":"...","agent_id":"...","scope":"...","timestamp_ms":1747728000000}}'
```

## Canonical derivation

```
action_ref = SHA-256(JCS(preimage_object))
```

Where JCS is [JSON Canonicalization Scheme (RFC 8785)](https://www.rfc-editor.org/rfc/rfc8785):
- Keys sorted lexicographically
- No whitespace
- Field names are opaque bytes (load-bearing in the digest)
- `timestamp_ms` (epoch integer) is the canonical timestamp field

## Cross-implementation reproduction

| Implementation | Language | Vectors | Source |
|---------------|----------|---------|--------|
| action-ref-verify | Node.js | 12/12 | andysalvo (this repo) |
| runner_python.py | Python | 12/12 | andysalvo (this repo) |
| vauban-zkpay-x402 | Rust | 9/9 + 3 proposed | seritalien |
| FeedOracle | Python | 3/3 sampled | feedoracle |
| AlgoVoi | Python/JS/Go/Java | 9/9 x4 impls | chopmob-cloud |

Five independent implementations across five languages reproduce identical digests from the same preimages with independent JCS canonicalization.

## Conformance vectors

| Vector | Result | Tests |
|--------|--------|-------|
| `0001-giskard-baseline` | PASS | Canonical 4-field derivation |
| `0002-ms-precision-trap` | FAIL | Float vs integer timestamp_ms |
| `0003-trailing-whitespace` | FAIL | Trailing space changes digest |
| `0004-extra-field-ignored` | PASS | Extra fields in preimage |
| `0005-key-order-resilience` | PASS | Key order doesn't affect digest |
| `0006-rfc8785-negative-zero` | PASS | timestamp_ms = 0 |
| `0007-rfc8785-key-sorting-stress` | PASS | Unicode in values |
| `0008-x402-2357-shared-fixture` | PASS | Cross-layer binding with payment_hash |
| `0009-field-name-load-bearing` | FAIL | timestamp vs timestamp_ms divergence |
| `0010-duplicate-key-rejection` | FAIL | Duplicate JSON keys (proposed by Vauban Pay) |
| `0011-unicode-nfd-divergence` | FAIL | NFC vs NFD encoding (proposed by Vauban Pay) |
| `0012-required-field-missing` | FAIL | Missing agent_id field (proposed by Vauban Pay) |

Vectors 0010-0012 proposed by seritalien (Vauban Pay) on [PR #2398](https://github.com/x402-foundation/x402/pull/2398).

See [CONFORMANCE_INTAKE.md](CONFORMANCE_INTAKE.md) for submission format.

## Built by

[Crest Deployment Systems](https://crestsystems.ai)
