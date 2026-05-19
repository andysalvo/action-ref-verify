# Contributing

## Submitting vectors

See [CONFORMANCE_INTAKE.md](CONFORMANCE_INTAKE.md) for the vector submission format and publication policy.

## Code contributions

1. Fork the repo
2. Create a branch from `main`
3. Run `node selftest.mjs` to verify your environment
4. Run `node verify.mjs vectors/0001-giskard-baseline.json` to confirm baseline passes
5. Submit a PR with a clear description

## Rules

- All changes to `vendor/canonicalize.mjs` require a signed commit and integrity hash update in CI
- All vectors must follow the schema in CONFORMANCE_INTAKE.md
- Negative/failing vectors are welcome and encouraged
- Do not submit vectors containing PII, production secrets, or private keys
- By submitting a vector, you agree to its public storage, reproduction, and publication of pass/fail results

## License

Contributions are accepted under Apache-2.0. See [LICENSE](LICENSE).
