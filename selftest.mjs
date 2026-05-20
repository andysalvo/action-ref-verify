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

const CANARY_MS = {
  input: {
    action_type: "sanctions_screen",
    agent_id: "did:web:agent-7.example.com",
    scope: "counterparty-due-diligence",
    timestamp_ms: 1747728000000
  },
  expected_canonical: '{"action_type":"sanctions_screen","agent_id":"did:web:agent-7.example.com","scope":"counterparty-due-diligence","timestamp_ms":1747728000000}',
  expected_hash: "10d8a38c01d8672176aa6e5209a368fde3e1831640d69e15283142b35880c2c1"
};

const jcsMs = canonicalize(CANARY_MS.input);
const hashMs = createHash("sha256").update(jcsMs, "utf8").digest("hex");

if (jcsMs !== CANARY_MS.expected_canonical) {
  console.error("CANARY_MS FAIL: canonical bytes diverged");
  console.error("  expected:", CANARY_MS.expected_canonical);
  console.error("  got:     ", jcsMs);
  failures++;
}

if (hashMs !== CANARY_MS.expected_hash) {
  console.error("CANARY_MS FAIL: hash diverged");
  console.error("  expected:", CANARY_MS.expected_hash);
  console.error("  got:     ", hashMs);
  failures++;
}

if (failures > 0) {
  console.error(`\nSELFTEST FAILED (${failures} failures). Verifier is not safe to use.`);
  process.exit(1);
}

console.log("SELFTEST PASS: both canaries verified (rfc3339 + epoch_ms)");
process.exit(0);
