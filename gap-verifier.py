#!/usr/bin/env python3
"""
Crest Gap Class Verifier v0.2

Verifies A2A #1734 v2 gap class commit-hash claims.
Supports single-commit and multi-commit (per-field citation) claims.

Scope (what this verifies):
- Commit exists in the claimed repository
- File exists at that commit
- Claimed content is present in the file
- JCS+SHA-256 derivations are correct

Scope (what this does NOT verify):
- Runtime behavior of any system
- Semantic truth of gap class claims
- Priority or authorship of contributions
- Legal or regulatory compliance

Usage:
  # Single commit
  python3 gap-verifier.py --inline '{"repo":"owner/repo","commit":"abc123","path":"file.md","contains":"text"}'

  # Multi-commit (per-field citations)
  python3 gap-verifier.py --inline '{"repo":"owner/repo","files":[{"commit":"abc123","path":"file.md","contains":"text","field":"base spec"},{"commit":"def456","path":"file2.md","contains":"other","field":"new field"}]}'
"""

import json
import hashlib
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone


def jcs(obj):
    if obj is None: return "null"
    if isinstance(obj, bool): return "true" if obj else "false"
    if isinstance(obj, int): return str(obj)
    if isinstance(obj, float): return json.dumps(obj)
    if isinstance(obj, str): return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list): return "[" + ",".join(jcs(i) for i in obj) + "]"
    if isinstance(obj, dict):
        keys = sorted(obj.keys())
        return "{" + ",".join(json.dumps(k, ensure_ascii=False) + ":" + jcs(obj[k]) for k in keys) + "}"


def sha256_hex(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def github_fetch(url):
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "crest-gap-verifier/0.1"
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read()
            return json.loads(body), resp.status, sha256_hex(body)
    except urllib.error.HTTPError as e:
        return None, e.code, None
    except Exception as e:
        return None, 0, str(e)


def verify_claim(claim):
    receipt = {
        "receipt_schema": "crest.a2a1734.gap_verification_receipt.v1",
        "verifier": {
            "name": "crest-gap-verifier",
            "version": "0.1.0",
            "url": "https://verify.crestsystems.ai",
            "policy": "fail-closed, content-only, no semantic claims"
        },
        "claim": claim,
        "checks": [],
        "warnings": [],
        "errors": [],
        "status": "pending",
        "conflict_disclosure": "Crest is cited as a canon_version adopter in gap class 4. This receipt discloses that conflict.",
        "explicit_non_claims": [
            "This receipt does not verify runtime behavior",
            "This receipt does not establish authorship priority",
            "This receipt does not validate semantic correctness of gap class claims",
            "This receipt proves only that specific content existed at a specific commit"
        ],
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    }

    repo = claim.get("repo", "")
    commit = claim.get("commit", "")
    path = claim.get("path", "")
    contains = claim.get("contains")
    derivation = claim.get("derivation")
    gap_class = claim.get("gap_class")

    if len(commit) < 40:
        receipt["warnings"].append(f"ABBREVIATED_COMMIT: '{commit}' is not a full SHA. Resolving via API.")

    # Check 1: Commit exists
    commit_url = f"https://api.github.com/repos/{repo}/commits/{commit}"
    commit_data, http_status, response_hash = github_fetch(commit_url)

    check1 = {
        "check": "commit_exists",
        "result": "pass" if http_status == 200 else "fail",
        "evidence": {
            "url": commit_url,
            "http_status": http_status,
            "response_sha256": response_hash
        }
    }

    if commit_data and http_status == 200:
        full_sha = commit_data.get("sha", commit)
        check1["evidence"]["resolved_sha"] = full_sha
        check1["evidence"]["commit_date"] = commit_data.get("commit", {}).get("committer", {}).get("date")
        check1["evidence"]["author"] = commit_data.get("commit", {}).get("author", {}).get("name")
        if full_sha != commit and len(commit) < 40:
            receipt["warnings"].append(f"RESOLVED: '{commit}' -> '{full_sha}'")
    else:
        receipt["errors"].append(f"Commit {commit} not found in {repo} (HTTP {http_status})")
        receipt["status"] = "fail"
        receipt["checks"].append(check1)
        receipt["receipt_id"] = "sha256:" + sha256_hex(jcs(receipt))
        return receipt

    receipt["checks"].append(check1)

    # Check 2: File exists at commit
    file_url = f"https://api.github.com/repos/{repo}/contents/{path}?ref={full_sha}"
    file_data, http_status, response_hash = github_fetch(file_url)

    check2 = {
        "check": "file_present_at_commit",
        "result": "pass" if http_status == 200 else "fail",
        "evidence": {
            "url": file_url,
            "http_status": http_status,
            "path": path
        }
    }

    if file_data and http_status == 200:
        import base64
        content_b64 = file_data.get("content", "")
        try:
            file_content = base64.b64decode(content_b64).decode("utf-8")
            check2["evidence"]["file_sha256"] = sha256_hex(file_content)
            check2["evidence"]["size_bytes"] = len(file_content)
        except Exception:
            file_content = ""
            check2["evidence"]["decode_error"] = True
    else:
        receipt["errors"].append(f"File {path} not found at commit {full_sha}")
        receipt["status"] = "fail"
        receipt["checks"].append(check2)
        receipt["receipt_id"] = "sha256:" + sha256_hex(jcs(receipt))
        return receipt

    receipt["checks"].append(check2)

    # Check 3: Content match (if contains assertion provided)
    if contains:
        found = contains in file_content
        check3 = {
            "check": "content_match",
            "result": "pass" if found else "fail",
            "evidence": {
                "search_string_sha256": sha256_hex(contains),
                "search_string_length": len(contains),
                "found": found
            }
        }
        receipt["checks"].append(check3)
        if not found:
            receipt["errors"].append(f"Content assertion not found in {path}")

    # Check 4: JCS+SHA-256 derivation (if provided)
    if derivation:
        preimage = derivation.get("preimage")
        expected_hash = derivation.get("expected_hash")

        if preimage and expected_hash:
            canonical = jcs(preimage)
            computed = sha256_hex(canonical)
            match = computed == expected_hash

            check4 = {
                "check": "jcs_sha256_derivation",
                "result": "pass" if match else "fail",
                "evidence": {
                    "canonicalization": "RFC8785",
                    "canonical_sha256": sha256_hex(canonical.encode("utf-8")),
                    "computed_digest": computed,
                    "expected_digest": expected_hash,
                    "match": match
                }
            }
            receipt["checks"].append(check4)
            if not match:
                receipt["errors"].append("JCS+SHA-256 derivation mismatch")

    # Determine overall status
    results = [c["result"] for c in receipt["checks"]]
    if "fail" in results:
        receipt["status"] = "fail"
    elif all(r == "pass" for r in results):
        receipt["status"] = "pass"
    else:
        receipt["status"] = "inconclusive"

    if receipt["warnings"]:
        if receipt["status"] == "pass":
            receipt["status"] = "pass_with_warnings"

    # Content-address the receipt
    receipt["receipt_id"] = "sha256:" + sha256_hex(jcs(receipt))

    return receipt


def verify_multi_commit(claim):
    """Verify a multi-commit claim with per-field commit citations."""
    repo = claim.get("repo", "")
    files = claim.get("files", [])

    results = {
        "receipt_schema": "crest.a2a1734.gap_verification_receipt.v2",
        "verifier": {
            "name": "crest-gap-verifier",
            "version": "0.2.0",
            "url": "https://verify.crestsystems.ai",
            "policy": "fail-closed, content-only, no semantic claims"
        },
        "claim": claim,
        "file_checks": [],
        "warnings": [],
        "errors": [],
        "conflict_disclosure": "Crest is cited as a canon_version adopter in gap class 4.",
        "explicit_non_claims": [
            "This receipt does not verify runtime behavior",
            "This receipt does not establish authorship priority",
            "This receipt does not validate semantic correctness",
            "Each file is verified at its cited commit independently"
        ],
        "created_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "receipt_ref": None
    }

    for entry in files:
        sub_claim = {
            "repo": repo,
            "commit": entry.get("commit", ""),
            "path": entry.get("path", ""),
            "contains": entry.get("contains"),
            "derivation": entry.get("derivation"),
            "field": entry.get("field", "")
        }
        sub_receipt = verify_claim(sub_claim)
        results["file_checks"].append({
            "path": entry.get("path"),
            "commit": entry.get("commit"),
            "field": entry.get("field", ""),
            "status": sub_receipt["status"],
            "checks": sub_receipt["checks"],
            "warnings": sub_receipt.get("warnings", []),
            "errors": sub_receipt.get("errors", [])
        })
        results["warnings"].extend(sub_receipt.get("warnings", []))
        results["errors"].extend(sub_receipt.get("errors", []))

    statuses = [fc["status"] for fc in results["file_checks"]]
    if "fail" in statuses:
        results["overall_status"] = "fail"
    elif all("pass" in s for s in statuses):
        results["overall_status"] = "pass"
    else:
        results["overall_status"] = "partial"

    passed = sum(1 for s in statuses if "pass" in s)
    results["summary"] = f"{passed}/{len(statuses)} files verified across {len(set(e.get('commit','') for e in files))} commits"

    canonical = jcs(results)
    results["receipt_ref"] = "sha256:" + sha256_hex(canonical)

    return results


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 gap-verifier.py claim.json")
        print("       python3 gap-verifier.py --inline '{...}'")
        print("  Single: {repo, commit, path, contains}")
        print("  Multi:  {repo, files: [{commit, path, contains, field}, ...]}")
        sys.exit(1)

    if sys.argv[1] == "--inline":
        claim = json.loads(sys.argv[2])
    else:
        with open(sys.argv[1]) as f:
            claim = json.load(f)

    if "files" in claim:
        receipt = verify_multi_commit(claim)
    else:
        receipt = verify_claim(claim)

    print(json.dumps(receipt, indent=2))

    status = receipt.get("overall_status", receipt.get("status", "fail"))
    if "pass" in status:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
