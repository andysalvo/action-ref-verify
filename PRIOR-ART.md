# Prior Art Record

Immutable timeline establishing the provenance of the `timestamp_ms` epoch-integer canonicalization convention and the field-name-load-bearing conformance proof (vector 0009) contributed by Andy Salvo / Crest Deployment Systems to the x402 ecosystem.

All links are GitHub comment permalinks (immutable, SHA-anchored).

## Timeline

### 2026-05-20

| Time (UTC) | Actor | Event | Permalink |
|-----------|-------|-------|-----------|
| 18:33 | andysalvo | Posted three-implementation consensus on `timestamp_ms` as canonical preimage field on #2357 | [issuecomment-4501468903](https://github.com/x402-foundation/x402/issues/2357#issuecomment-4501468903) |
| 18:58 | andysalvo | Identified timestamp precision failure mode on #2326: `"2026-05-19T06:00:00Z"` vs `"2026-05-19T06:00:00.000Z"` produce different JCS digests. Proposed pinning the lexical format. | [issuecomment-4501663969](https://github.com/x402-foundation/x402/issues/2326#issuecomment-4501663969) |
| 19:16 | chopmob-cloud | Responded on #2326 citing andysalvo directly: "@andysalvo -- the 'JCS is necessary but not sufficient; need schema normalization + JCS' framing is exactly right" and "Your timestamp-precision case is the natural sixth pair invariant" | [issuecomment-4501797571](https://github.com/x402-foundation/x402/issues/2326#issuecomment-4501797571) |
| 19:21 | seritalien | Concurred on #2357: "Concur on `timestamp_ms` (epoch integer) as the canonical preimage field." | #2357 thread |
| 19:55 | feedoracle | Concurred on #2357: "Concur on `timestamp_ms` (epoch integer) as the canonical preimage field. Same read on our side." | #2357 thread |

### 2026-05-21

| Time (UTC) | Actor | Event | Permalink |
|-----------|-------|-------|-----------|
| 02:38 | chopmob-cloud | Shipped attestation conformance vectors on #2326 using `timestamp_ms` as the 6th invariant. Cited: "Cross-reference: this set documents the timestamp-lexical invariant from the attestation layer; @andysalvo's PR #2398 vector 0009 documents the same invariant from the work-receipt layer." | [issuecomment-4504289607](https://github.com/x402-foundation/x402/issues/2326#issuecomment-4504289607) |
| 20:59 | andysalvo | Opened PR #2398 on x402-foundation/x402: 9 conformance vectors including vector 0009 (field-name-load-bearing). First `fixtures/` directory in the repo. | [PR #2398](https://github.com/x402-foundation/x402/pull/2398) |

### 2026-05-22

| Time (UTC) | Actor | Event |
|-----------|-------|-------|
| 15:15 | chopmob-cloud | First use of identifier `jcs-rfc8785-v1` in PR #2436 on x402-foundation/x402 |

### 2026-05-23

| Time (UTC) | Actor | Event | Permalink |
|-----------|-------|-------|-----------|
| 18:06 | chopmob-cloud | On #2421, validated andysalvo's risk-check implementation: "the implementation looks right," invited contribution to conformance vectors repo | [issuecomment-4526155766](https://github.com/x402-foundation/x402/issues/2421#issuecomment-4526155766) |

### 2026-05-24

| Time (UTC) | Actor | Event |
|-----------|-------|-------|
| -- | chopmob-cloud | Closed PR #2436 (shared canonicalization section) on x402-foundation/x402 |
| -- | chopmob-cloud | Published `draft-hopley-x402-compliance-receipt-00` and `draft-hopley-x402-refund-receipt-00` on IETF datatracker. Both use `timestamp_ms` convention and `jcs-rfc8785-v1` identifier. Acknowledgments credit FeedOracle and Vauban Pay. Zero mention of andysalvo, Crest, PR #2398, or vector 0009. |
| -- | chopmob-cloud | Published `draft-hopley-x402-canonicalisation-jcs-v1-00` on IETF datatracker, claiming the canonicalization discipline as sole AlgoVoi work. |
| 16:47 | chopmob-cloud | Closed PR #1 on chopmob-cloud/algovoi-jcs-conformance-vectors. Rejected andysalvo's contributed vectors. Stated: "Going forward chopmob-cloud/algovoi-jcs-conformance-vectors is maintained under sole AlgoVoi authorship." | [PR #1](https://github.com/chopmob-cloud/algovoi-jcs-conformance-vectors/pull/1) |
| -- | chopmob-cloud | Offered to cross-link to andysalvo's work as a "downstream-adopter artefact" -- framing andysalvo as a consumer of AlgoVoi's discipline rather than a co-contributor. |
| -- | chopmob-cloud | Did not address the attribution correction request for IETF drafts. |

## What is established

1. andysalvo identified the timestamp precision failure mode on x402-foundation/x402 #2326 before chopmob-cloud adopted it.
2. chopmob-cloud explicitly cited andysalvo's contribution twice by name before publishing IETF drafts without attribution.
3. andysalvo opened the first `fixtures/` directory and first cross-language conformance vectors on x402-foundation/x402 (PR #2398) before chopmob-cloud's IETF submissions.
4. Vector 0009 (field-name-load-bearing) was created by andysalvo and proves the convention that all three IETF drafts rely on.
5. chopmob-cloud invited andysalvo to contribute vectors, then rejected the contribution and claimed sole authorship.

## What is NOT claimed

- The `timestamp_ms` field name is not copyrightable.
- Apache-2.0 permits reuse of technical conventions.
- This is not a legal claim. It is a factual provenance record.

## Crest artifacts

- PR #2398: https://github.com/x402-foundation/x402/pull/2398
- action-ref-verify: https://github.com/andysalvo/action-ref-verify (v0.4.0, 12 vectors, 2 language runners)
- verify.crestsystems.ai: live conformance verification API
- supership.crestsystems.ai: live risk-check provider (service_trust category)
- Provenance document: docs/provenance/2026-05-24-ietf-attribution.md in andysalvo/crest
