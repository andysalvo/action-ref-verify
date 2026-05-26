# Implementation Notes: Conformance Verification for Agent Commerce

Artifact 3 for A2A v0.4 coordination. Observations from building and running conformance infrastructure across x402, A2A, and AP2.

## Run the vectors

```bash
npx @crestdeploymentsystems/verify https://your-endpoint.com
```

Or paste a JSON preimage at [verify.crestsystems.ai](https://verify.crestsystems.ai).

## What we verify

5 checks per endpoint:

1. **Liveness** -- is the endpoint reachable?
2. **x402 challenge** -- does it return HTTP 402 with payment headers?
3. **Trust history** -- is it in the 47,814-service on-chain index?
4. **Network passport** -- observed payment history on Base mainnet
5. **Discovery** -- does it publish `/.well-known/agent.json`?

12 conformance vectors test JCS (RFC 8785) canonicalization: key ordering, timestamp precision, nested objects, arrays, null handling, boolean serialization, float precision, field-name sensitivity.

## Vectors in the Foundation repo

[PR #2398](https://github.com/x402-foundation/x402/pull/2398) -- 12 vectors for work-receipt binding via `action_ref = SHA-256(JCS(preimage))`.

14 additional vectors in the [transactional claim_type draft](https://verify.crestsystems.ai/transactional-draft-00.json) covering the full lifecycle (issuance, verification, execution, revocation, settlement) plus 8 adversarial cases.

## Known findings

### AP2 Unicode normalization (vectors 006a, 006b)

Running AlgoVoi's AP2 OMH v0 vectors against action-ref-verify: 5/7 pass, 2 diverge on Unicode NFC/NFD vectors.

Our JCS implementation follows RFC 8785: canonicalize but do not pre-normalize Unicode. The expected hashes in vectors 006a and 006b imply NFC pre-normalization before canonicalization.

**Open question for AP2:** if mandates carry Unicode strings, does AP2 require NFC normalization prior to JCS? At which layer?

Full results: [verify.crestsystems.ai/ap2-omh-v0-results.json](https://verify.crestsystems.ai/ap2-omh-v0-results.json)

### timestamp_ms convention

The `timestamp_ms` epoch-integer convention (Substrate Rule 2 in draft-hopley-x402-canonicalisation-jcs-v1-02) was first posted on [x402 #2357](https://github.com/x402-foundation/x402/issues/2357) on 2026-05-20. Three independent implementations (Rust, Python, Node.js) converged on epoch integer over RFC 3339 string. This avoids lexical ambiguity under JCS serialization.

Vector 0009 (`field-name-load-bearing`) demonstrates this: `timestamp` and `timestamp_ms` produce different hashes. The field name is part of the canonical form.

### Honest nulls

When a service is not in the on-chain index, we return `score: null` with a `null_reason`:

- `unknown_service` -- no observed x402 payment activity
- `insufficient_signal` -- exists but not enough data for a score
- `evaluation_failed` -- internal error
- `no_query_subject` -- no URL or wallet provided

We never fabricate scores. 47,814 services indexed from on-chain USDC flows. Zero self-reported.

## Trust-check response shape

`urn:crest:trust-check-v1` -- JCS-canonicalized, Ed25519-signed envelopes with:

- `query_ref` / `response_ref`: SHA-256 content-addressed integrity
- `freshness`: `issued_at`, `expires_at`, `index_as_of`, `index_snapshot_id`
- `evidence[]`: typed array with `{kind, source, ref, observed_at, weight}`
- `null_reason`: informative nulls (4-value taxonomy)

Schema: `GET supership.crestsystems.ai/v1/spec`

## Provenance

- Conformance vectors: [andysalvo/action-ref-verify](https://github.com/andysalvo/action-ref-verify) (commit 8b73ac9)
- Foundation PR: [x402-foundation/x402 #2398](https://github.com/x402-foundation/x402/pull/2398)
- IETF credits: submissions 163527, 163528, 163529 (draft-hopley-x402-canonicalisation-jcs-v1-02, compliance-receipt-02, refund-receipt-02)
- npm package: [@crestdeploymentsystems/verify](https://www.npmjs.com/package/@crestdeploymentsystems/verify) v0.1.0

## Author

Andy Salvo / Crest Deployment Systems LLC
https://verify.crestsystems.ai
