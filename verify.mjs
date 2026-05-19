#!/usr/bin/env node
/**
 * action-ref conformance verifier
 *
 * Re-derives action_ref using JCS (RFC 8785) + SHA-256
 * and verifies it matches the claimed hash.
 *
 * Usage:
 *   node verify.mjs fixture.json
 *   echo '{"action_ref":"...","preimage":{...}}' | node verify.mjs
 */

import { createHash } from "crypto";
import { readFileSync } from "fs";
import canonicalize from "./vendor/canonicalize.mjs";

function deriveActionRef(preimage) {
  const { agent_id, action_type, scope, timestamp } = preimage;
  if (!agent_id || !action_type || !scope || !timestamp) {
    return { error: "Missing required preimage fields: agent_id, action_type, scope, timestamp" };
  }
  const obj = { action_type, agent_id, scope, timestamp };
  const jcs = canonicalize(obj);
  return { hash: createHash("sha256").update(jcs, "utf8").digest("hex"), canonical: jcs };
}

function verify(fixture) {
  const results = [];

  if (fixture.preimage) {
    const derived = deriveActionRef(fixture.preimage);
    if (derived.error) {
      results.push({ check: "action_ref_derivation", status: "FAIL", reason: derived.error });
    } else {
      const claimed = (fixture.action_ref || "").replace(/^0x/, "");
      const match = derived.hash === claimed;
      results.push({
        check: "action_ref_derivation",
        status: match ? "PASS" : "FAIL",
        claimed: claimed.slice(0, 16) + "...",
        derived: derived.hash.slice(0, 16) + "...",
        canonical_input: derived.canonical,
        method: "JCS (RFC 8785) + SHA-256",
      });
    }
  }

  if (fixture.payment_hash) {
    results.push({
      check: "payment_hash_present",
      status: "PASS",
      hash: fixture.payment_hash.slice(0, 16) + "...",
    });
  } else {
    results.push({ check: "payment_hash_present", status: "SKIP", reason: "No payment_hash in fixture" });
  }

  if (fixture.spec) {
    results.push({ check: "spec_declared", status: "PASS", spec: fixture.spec });
  }

  const failed = results.filter(r => r.status === "FAIL").length;
  const passed = results.filter(r => r.status === "PASS").length;

  return {
    verdict: failed > 0 ? "FAIL" : "PASS",
    checks: results.length,
    passed,
    failed,
    results,
  };
}

let input;
const arg = process.argv[2];
if (arg && arg !== "-") {
  input = JSON.parse(readFileSync(arg, "utf-8"));
} else {
  input = JSON.parse(readFileSync("/dev/stdin", "utf-8"));
}

const fixtures = Array.isArray(input) ? input : [input];
for (const f of fixtures) {
  const result = verify(f);
  console.log(JSON.stringify(result, null, 2));
}
