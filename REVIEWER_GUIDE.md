# Reviewer Guide for PR #2398

This PR adds conformance fixtures for `action_ref` work-receipt binding to `x402-foundation/x402` under `fixtures/action-ref-verify/v0/`.

## What this PR adds

- 9 JSON vector files under `fixtures/action-ref-verify/v0/vectors/`
- A manifest (`manifest.json`) listing all vectors and their expected results
- A README explaining the derivation, vector table, and reproduction instructions
- A top-level `fixtures/README.md` defining the fixture directory structure

No code changes. No dependencies. No CI modifications. Data only.

## How to verify (3 commands)

```bash
# 1. Clone the source repo
git clone https://github.com/andysalvo/action-ref-verify.git
cd action-ref-verify && npm install

# 2. Run all vectors
node run-all.mjs

# 3. Check result
# Expected: "12 vectors | 12 conformant | 0 non-conformant"
```

Or with Python:
```bash
pip install rfc8785
python3 runner_python.py
# Expected: "12/12 conformant"
```

## What this PR does NOT add

- No spec text or normative language
- No SDK changes
- No CI workflows
- No runtime dependencies
- No payment-flow modifications

## Derivation

```
action_ref = SHA-256(JCS(preimage))
```

Where JCS = JSON Canonicalization Scheme ([RFC 8785](https://www.rfc-editor.org/rfc/rfc8785)). The preimage is a JSON object with fields: `action_type`, `agent_id`, `scope`, `timestamp_ms` (epoch integer).

## Key vectors

| Vector | Tests | Why it matters |
|--------|-------|----------------|
| 0001 | Canonical baseline | Happy path -- all implementations must produce this digest |
| 0008 | Cross-layer binding | Same `payment_hash` + `action_ref` verified across Rust, Python, Node.js |
| 0009 | Field-name divergence | Proves `timestamp` vs `timestamp_ms` produce different digests (load-bearing) |

## Independent reproductions

This vector set has been independently reproduced by 5 implementations across 5 languages:

| Implementation | Language | Result |
|---------------|----------|--------|
| action-ref-verify (this repo) | Node.js | 12/12 |
| runner_python.py (this repo) | Python | 12/12 |
| vauban-zkpay-x402 | Rust | 9/9 + 3 proposed |
| FeedOracle | Python | 3/3 sampled |
| AlgoVoi | Python/JS/Go/Java | 9/9 x4 impls |

## Layout

The `fixtures/` directory is designed for additional conformance suites to land alongside:

```
fixtures/
  README.md                          # Directory structure
  action-ref-verify/
    v0/
      README.md
      manifest.json
      vectors/
        0001-baseline.json
        ...
        0009-field-name-load-bearing.json
```

## Source

[action-ref-verify v0.4.0](https://github.com/andysalvo/action-ref-verify) (Apache-2.0).
