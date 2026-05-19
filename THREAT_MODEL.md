# Threat Model

## What we defend

The action-ref conformance harness produces verdicts (PASS/FAIL/CONFORMANT/NON-CONFORMANT) that other implementations may rely on to validate their action_ref derivations. A wrong verdict has real consequences: an implementation marked PASS may be deployed into production with an incorrect hash, or an implementation marked FAIL may be rejected when it is actually correct.

## Adversary classes

### 1. Malicious vector submitter
**Goal:** Submit a vector designed to produce a false PASS, making the harness endorse an incorrect implementation.
**Controls:** Schema validation, 4-field extraction (extra fields ignored), vendored canonicalization with integrity check, self-test canary. Vectors are run deterministically; the submitter cannot influence the verifier logic.

### 2. Supply chain attacker
**Goal:** Compromise the canonicalization dependency to silently alter hash output.
**Controls:** canonicalize@3.0.0 is vendored (not fetched from npm at runtime). SHA-256 integrity hash checked in CI. Self-test canary runs against a known-good vector before every verification. Any canonicalization drift fails the build.

### 3. Spec drift attacker
**Goal:** Evolve the spec in a way that invalidates existing conformance verdicts without detection.
**Controls:** Every verdict is anchored to a spec version and harness commit. Historical verdicts are immutable. CONFORMANCE_INTAKE.md requires vectors to declare the spec version they target.

### 4. Dispute gaming attacker
**Goal:** Exploit the dispute process to force removal of a legitimate FAIL verdict.
**Controls:** Dispute process (see CONFORMANCE_INTAKE.md) requires reproduction evidence. Verdicts are not removed; they are superseded by new verdicts with updated spec/harness references.

### 5. Canonicalization edge case attacker
**Goal:** Find a JSON input where our JCS implementation diverges from RFC 8785, producing a silently wrong hash.
**Controls:** Vendored implementation tested against RFC 8785 Appendix B reference vectors. Adversarial vectors targeting known JCS edge cases (negative zero, Unicode sorting, number serialization, key ordering). CI matrix runs on Node 18/20/22 to catch runtime-specific behavior.

## Out of scope

- Network attacks on hosted endpoints (the CLI is the source of truth, not any API)
- Compromise of the GitHub account (standard GitHub security practices apply)
- Attacks on the x402 protocol itself (we verify conformance to the spec, not the spec's correctness)

## Open risks

- The vendored JCS implementation has not been formally audited against the complete RFC 8785 test suite (Appendix B has 18 test groups; we cover the most critical ones)
- No memory-safe implementation exists; the Node.js runtime is the trust boundary
- The conformance page is manually maintained; automated generation from CI artifacts is planned
