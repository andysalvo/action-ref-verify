#!/usr/bin/env node
import { readFileSync, readdirSync } from "fs";
import { createHash } from "crypto";
import canonicalize from "./vendor/canonicalize.mjs";

const vectorDir = new URL("./vectors/", import.meta.url);
const files = readdirSync(vectorDir).filter(f => f.endsWith(".json")).sort();

let total = 0, conformant = 0, nonconformant = 0;

console.log("ACTION-REF CONFORMANCE REPORT");
console.log(`Harness: action-ref-verify v0.3.0`);
console.log(`Date: ${new Date().toISOString()}`);
console.log("=".repeat(72));
console.log();

for (const file of files) {
  const fixture = JSON.parse(readFileSync(new URL(file, vectorDir), "utf-8"));
  const { action_type, agent_id, scope } = fixture.preimage;
  const hasTimestampMs = Object.prototype.hasOwnProperty.call(fixture.preimage, "timestamp_ms");

  const obj = hasTimestampMs
    ? { action_type, agent_id, scope, timestamp_ms: fixture.preimage.timestamp_ms }
    : { action_type, agent_id, scope, timestamp: fixture.preimage.timestamp };
  const jcs = canonicalize(obj);
  const computed = createHash("sha256").update(jcs, "utf8").digest("hex");
  const claimed = (fixture.action_ref || "").replace(/^0x/, "");
  const hashMatch = computed === claimed;

  const expected = fixture.expected_result || "PASS";
  const actual = hashMatch ? "PASS" : "FAIL";
  const conformance = actual === expected ? "CONFORMANT" : "NON-CONFORMANT";

  total++;
  if (conformance === "CONFORMANT") conformant++;
  else nonconformant++;

  console.log(`VECTOR:     ${fixture.name}`);
  console.log(`FILE:       ${file}`);
  console.log(`IMPL:       ${fixture.implementation}`);
  console.log(`EXPECTED:   ${expected}`);
  console.log(`ACTUAL:     ${actual}`);
  console.log(`CONFORMANT: ${conformance}`);
  console.log(`CANONICAL:  ${jcs}`);
  console.log(`CLAIMED:    ${claimed}`);
  console.log(`COMPUTED:   ${computed}`);
  if (!hashMatch) {
    console.log(`DIFF:       hashes diverge (expected by design for FAIL vectors)`);
  } else {
    console.log(`DIFF:       none`);
  }
  if (fixture.notes) console.log(`NOTES:      ${fixture.notes}`);
  console.log("-".repeat(72));
  console.log();
}

console.log("=".repeat(72));
console.log(`SUMMARY: ${total} vectors | ${conformant} conformant | ${nonconformant} non-conformant`);
if (nonconformant > 0) {
  console.log("STATUS: NON-CONFORMANT VECTORS DETECTED");
  process.exit(1);
} else {
  console.log("STATUS: ALL VECTORS CONFORMANT");
}
