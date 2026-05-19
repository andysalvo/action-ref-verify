#!/usr/bin/env node
import { createHash } from "crypto";
import canonicalize from "./vendor/canonicalize.mjs";

const CANARY = {
  input: {
    action_type: "oracle.signal",
    agent_id: "nexus-agent-xa12.onrender.com",
    scope: "BTC",
    timestamp: "2025-05-18T11:40:31.000Z"
  },
  expected_canonical: '{"action_type":"oracle.signal","agent_id":"nexus-agent-xa12.onrender.com","scope":"BTC","timestamp":"2025-05-18T11:40:31.000Z"}',
  expected_hash: "fdd7f810499f06be24355ca8e2bfb8c4b965cc80c838f41fa074683443d89f5a"
};

const jcs = canonicalize(CANARY.input);
const hash = createHash("sha256").update(jcs, "utf8").digest("hex");

let failures = 0;

if (jcs !== CANARY.expected_canonical) {
  console.error("CANARY FAIL: canonical bytes diverged");
  console.error("  expected:", CANARY.expected_canonical);
  console.error("  got:     ", jcs);
  failures++;
}

if (hash !== CANARY.expected_hash) {
  console.error("CANARY FAIL: hash diverged");
  console.error("  expected:", CANARY.expected_hash);
  console.error("  got:     ", hash);
  failures++;
}

if (failures > 0) {
  console.error(`\nSELFTEST FAILED (${failures} failures). Verifier is not safe to use.`);
  process.exit(1);
}

console.log("SELFTEST PASS: canonicalize + SHA-256 canary verified");
process.exit(0);
