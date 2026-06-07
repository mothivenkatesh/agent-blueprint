---
name: reliability-and-failure
description: >
  Specify an agent's reliability, latency, and failure handling, and run a failure premortem.
  Use when defining retries/timeouts/idempotency, a latency budget, compensation/rollback, or
  enumerating how an agent breaks and how it degrades. A differentiator section. Writes PRD §9
  in the agent-blueprint pack.
allowed-tools: Read, Write, Edit
---

# reliability-and-failure  ★ (PRD §9)

Read `../../CLAUDE.md` first.

## When to use
For any agent going to production, especially with tools that take real-world actions.

## Method
1. Apply the 4-layer model: task retry (count, backoff) → task timeout (poll/response/total)
   → workflow timeout → compensation / failure-workflow. Add rate limits per heavy tool.
2. Idempotency: every side-effecting tool gets a stable business-identity key + dedupe store
   (retry without idempotency = duplicate charges).
3. Latency budget: set a target; for any step that can exceed ~30-60s (long LLM/agent runs),
   use async-invoke + poll, not a stretched timeout. Mind the ~60s LLM-task read timeout.
4. Failure premortem: list the failure modes (hallucination, runaway loop, tool failure,
   rate limit, cost blowup, context rot, silent regression) and a mitigation for each.
5. Degrade predictably: fall through on non-critical timeouts; abort on corrupted state.

## Output (PRD §9)
Retry/timeout/rate-limit policy + idempotency plan + latency budget + a failure-mode →
mitigation table (the premortem) + compensation/rollback design.

## Do / Don't (full list in CLAUDE.md)
- DO set all four reliability layers; DO make side-effecting tools idempotent; DO write the premortem.
- DON'T retry without idempotency; DON'T stretch timeouts for long tasks; DON'T assume the happy path.

## Hand off to
`model-and-cost` · `observability-and-ops`.

## Evidence
`references/skill-evidence-map.md` (Orkes 4-layer retry/timeout + saga/compensation + idempotency/TryStart; LLM 60s timeout) ·
`references/gap-closed-synthesis.md` (Mastra model fallback; "fail open"; degrade-predictably).
