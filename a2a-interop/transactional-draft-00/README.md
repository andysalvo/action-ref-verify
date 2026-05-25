# Transactional claim_type Conformance Suite (DRAFT)

Candidate test suite for the v0.4 `transactional` claim_type evidence-envelope format, submitted for review.

**Status:** CANDIDATE (draft-00)

## Vectors

14 vectors across 3 categories:

| Category | Count | Tests |
|----------|-------|-------|
| Positive | 5 | Full lifecycle: issuance, verification, execution, revocation, settlement |
| Stability | 1 | Determinism check (identical preimage = identical hash) |
| Adversarial | 8 | Timestamp precision, agent replay, field injection, empty string, null handling, nested objects, float precision, array ordering |

7 pair invariants enforce that adversarial mutations produce different hashes.

## Derivation

```
action_ref = SHA-256(JCS(preimage))
```

- JCS: RFC 8785 canonicalization
- Hash: SHA-256, lowercase hex
- Timestamps: `timestamp_ms` as epoch-millisecond integer

## How to validate

```bash
node -e "
const fs = require('fs');
const crypto = require('crypto');
function jcs(o){if(o===null)return'null';if(typeof o==='boolean')return o.toString();if(typeof o==='number')return JSON.stringify(o);if(typeof o==='string')return JSON.stringify(o);if(Array.isArray(o))return'['+o.map(jcs).join(',')+']';return'{'+Object.keys(o).sort().map(k=>JSON.stringify(k)+':'+jcs(o[k])).join(',')+'}'}
const suite = JSON.parse(fs.readFileSync('transactional-draft-00.json'));
let pass=0;
suite.vectors.forEach(v=>{const d=crypto.createHash('sha256').update(jcs(v.preimage)).digest('hex');const ok=d===v.action_ref;console.log(ok?'PASS':'FAIL',v.vector_id,v.name);if(ok)pass++});
console.log(pass+'/'+suite.vectors.length+' passed');
"
```

## Live results

Published at [verify.crestsystems.ai/transactional-draft-00.json](https://verify.crestsystems.ai/transactional-draft-00.json)

## Context

- [A2A #1734](https://github.com/a2aproject/A2A/discussions/1734) -- v0.4 coordination thread
- [PR #2398](https://github.com/x402-foundation/x402/pull/2398) -- Fixtures on x402-foundation
- [action-ref-verify](https://github.com/andysalvo/action-ref-verify) -- Source repo

## Author

Andy Salvo / Crest Deployment Systems LLC
https://verify.crestsystems.ai
