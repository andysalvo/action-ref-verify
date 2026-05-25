# A2A v0.4 Cross-Validation Fixtures

Cross-validation fixture exchange for the transactional `claim_type` evidence-envelope format, per the v0.4 coordination on [A2A #1734](https://github.com/a2aproject/A2A/discussions/1734).

## Structure

```
a2a-interop/
  agent-os/
    crest-produced/           # Fixtures we generate for Agent OS to validate
      transactional-lifecycle-v0.json
    agent-os-pending/         # Slot for Agent OS fixtures we will validate
  README.md
  RECIPROCITY.md
```

## Derivation

All fixtures use the shared derivation confirmed by both parties:

```
action_ref = SHA-256(JCS(preimage))
```

- JCS: RFC 8785 canonicalization
- Hash: SHA-256, lowercase hex
- Timestamps: `timestamp_ms` as epoch-millisecond integer

## Vectors

| # | Name | Lifecycle | Tests |
|---|------|-----------|-------|
| 1 | committed-claim-issuance | issuance | Claim created |
| 2 | committed-claim-verification | verification | Claim verified by arbiter |
| 3 | committed-claim-execution | execution | Claim acted upon |
| 4 | committed-claim-revocation | revocation | Claim revoked |
| 5 | lifecycle-stability-check | stability | Same preimage as #1 -- hash MUST match |
| 6 | timestamp-ms-1ms-precision | adversarial | 1ms offset -- hash MUST differ |
| 7 | replay-different-agent | adversarial | Different agent_id -- hash MUST differ |
| 8 | dual-timestamp-envelope | envelope | authority_verified_at_ms + revocation_check_at_ms |

## How to validate

```bash
# Node.js
node -e "
const fs = require('fs');
const crypto = require('crypto');
function jcs(o){if(o===null)return'null';if(typeof o==='boolean')return o.toString();if(typeof o==='number')return JSON.stringify(o);if(typeof o==='string')return JSON.stringify(o);if(Array.isArray(o))return'['+o.map(jcs).join(',')+']';return'{'+Object.keys(o).sort().map(k=>JSON.stringify(k)+':'+jcs(o[k])).join(',')+'}'}
const vectors = JSON.parse(fs.readFileSync('a2a-interop/agent-os/crest-produced/transactional-lifecycle-v0.json'));
let pass=0;
vectors.forEach(v=>{const d=crypto.createHash('sha256').update(jcs(v.preimage)).digest('hex');const ok=d===v.action_ref;console.log(ok?'PASS':'FAIL',v.name,d.slice(0,16)+'...');if(ok)pass++});
console.log(pass+'/'+vectors.length+' passed');
"
```

## Context

- [A2A #1734](https://github.com/a2aproject/A2A/discussions/1734) -- RFC thread
- [PR #2398](https://github.com/x402-foundation/x402/pull/2398) -- Fixtures on x402-foundation
- [action-ref-verify](https://github.com/andysalvo/action-ref-verify) -- Source repo
