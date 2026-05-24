#!/usr/bin/env python3
"""
Cross-language conformance runner for action-ref-verify vectors.
Validates SHA-256(JCS(preimage)) derivation using Python rfc8785.

Usage:
    pip install rfc8785
    python3 runner_python.py

Reads all vectors from vectors/*.json, computes JCS + SHA-256,
and reports PASS/FAIL against expected digests.
"""

import json
import hashlib
import os
import sys

try:
    from rfc8785 import dumps as jcs_dumps
except ImportError:
    print("ERROR: pip install rfc8785")
    sys.exit(1)

VECTORS_DIR = os.path.join(os.path.dirname(__file__), "vectors")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_vector(path: str) -> dict:
    with open(path) as f:
        v = json.load(f)

    name = v.get("name", os.path.basename(path))
    expected_result = v.get("expected_result", "PASS")
    expected_hash = v.get("action_ref") or v.get("expected_digest", "")
    preimage = v.get("preimage", {})

    canonical = jcs_dumps(preimage)
    computed = sha256_hex(canonical)
    matches = computed == expected_hash

    conformant = matches if expected_result == "PASS" else not matches

    return {
        "name": name,
        "expected": expected_result,
        "computed": computed[:16] + "...",
        "conformant": conformant,
    }


def main():
    if not os.path.isdir(VECTORS_DIR):
        print("ERROR: vectors/ directory not found")
        sys.exit(1)

    files = sorted(f for f in os.listdir(VECTORS_DIR) if f.endswith(".json"))
    if not files:
        print("ERROR: no vector files found")
        sys.exit(1)

    print(f"action-ref-verify Python runner")
    print(f"Vectors: {len(files)}")
    print(f"Engine: rfc8785 + hashlib.sha256")
    print("=" * 60)

    passed = 0
    failed = 0

    for f in files:
        result = verify_vector(os.path.join(VECTORS_DIR, f))
        status = "PASS" if result["conformant"] else "FAIL"
        if result["conformant"]:
            passed += 1
        else:
            failed += 1
        print(f"  {status}  {result['name']:<35} {result['expected']:<6} {result['computed']}")

    print("=" * 60)
    print(f"RESULT: {passed}/{passed + failed} conformant")

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
