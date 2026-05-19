# Profile: action-ref-v1-jcs-sha256

Canonical derivation of `action_ref` using JCS (RFC 8785) + SHA-256.

## Spec

- Source: [argentum-core/docs/spec/action-ref.md](https://github.com/giskard09/argentum-core/blob/main/docs/spec/action-ref.md)
- Encoding: JSON Canonicalization Scheme (RFC 8785)
- Hash: SHA-256
- Key ordering: Lexicographic (alphabetical for ASCII keys)
- Timestamp: RFC 3339 UTC with 3-digit millisecond precision

## Derivation

```
action_ref = SHA-256(JCS(preimage_object))
```

Where `preimage_object` contains: `action_type`, `agent_id`, `scope`, `timestamp`.

## Vectors

See `vectors/` in repo root. All vectors with `spec: "action-ref-v1-jcs-sha256"` are tested against this profile.
