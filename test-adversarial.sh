#!/bin/bash
# Adversarial test suite for gap-verifier
# Run: bash test-adversarial.sh
# All tests should produce the expected result (FAIL or PASS)

PASS=0
FAIL=0

check() {
  local name="$1" expected="$2" actual="$3"
  if [ "$expected" = "$actual" ]; then
    echo "  PASS: $name (expected=$expected)"
    PASS=$((PASS + 1))
  else
    echo "  FAIL: $name (expected=$expected got=$actual)"
    FAIL=$((FAIL + 1))
  fi
}

echo "=== Gap Verifier Adversarial Test Suite ==="
echo ""

# Tests that should FAIL
for test in \
  'nonexistent-repo|fail|{"repo":"doesnotexist/fakerepo","commit":"abc123","path":"README.md"}' \
  'invalid-commit|fail|{"repo":"andysalvo/action-ref-verify","commit":"0000000000000000000000000000000000000000","path":"README.md"}' \
  'nonexistent-file|fail|{"repo":"andysalvo/action-ref-verify","commit":"HEAD","path":"this/does/not/exist.md"}' \
  'false-content|fail|{"repo":"andysalvo/action-ref-verify","commit":"HEAD","path":"README.md","contains":"THIS_STRING_DOES_NOT_EXIST_ANYWHERE"}' \
  'empty-claim|fail|{}' \
  'wrong-derivation|fail|{"repo":"andysalvo/action-ref-verify","commit":"HEAD","path":"README.md","derivation":{"preimage":{"test":true},"expected_hash":"0000000000000000000000000000000000000000000000000000000000000000"}}' \
  'private-repo|fail|{"repo":"andysalvo/crest","commit":"HEAD","path":"README.md"}'; do

  name=$(echo "$test" | cut -d'|' -f1)
  expected=$(echo "$test" | cut -d'|' -f2)
  claim=$(echo "$test" | cut -d'|' -f3-)
  actual=$(python3 gap-verifier.py --inline "$claim" 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print('pass' if 'pass' in d['status'] else 'fail')" 2>/dev/null || echo "error")
  check "$name" "$expected" "$actual"
done

# Tests that should PASS
actual=$(python3 gap-verifier.py --inline '{"repo":"giskard09/argentum-core","commit":"71c01e8","path":"docs/spec/action-ref.md","contains":"action_ref"}' 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print('pass' if 'pass' in d['status'] else 'fail')" 2>/dev/null || echo "error")
check "real-content-pass" "pass" "$actual"

echo ""
echo "=== Results: $PASS passed, $FAIL failed ==="
exit $FAIL
