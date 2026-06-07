---
name: safety-and-guardrails
description: >
  Specify an agent's trust, safety, security, and compliance. Use when designing guardrails
  against prompt injection / PII / jailbreaks, planning RBAC and secrets, sandboxing
  agent-run code, setting spend caps, or meeting compliance. Writes PRD §8 in the agent-builder pack.
allowed-tools: Read, Write, Edit
---

# safety-and-guardrails  (PRD §8)

Read `../../CLAUDE.md` first.

## When to use
For any agent with external input, real-world actions, sensitive data, or code execution.

## Method
1. Input guardrails: prompt-injection detection, jailbreak resistance, PII redaction,
   off-topic/abuse filtering. (Agents that browse/read docs can ingest malicious instructions.)
2. Output guardrails: authorization check, data-leakage scrub, toxicity, hallucination catch.
3. Failure posture: fail OPEN by default (don't block legit users on a guardrail error),
   fail CLOSED for security (prompt-injection, auth). Order deterministic checks before LLM ones.
4. Access & isolation: RBAC (least privilege per agent + per user), secrets server-side
   (never in prompts), sandbox any agent-generated code (contained blast radius), spend caps.
5. Audit trail: log every decision/action for compliance.

## Output (PRD §8)
Guardrail list (input/output, fail-open vs fail-closed) + RBAC + secrets + sandbox + spend cap + audit plan.

## Do / Don't (full list in CLAUDE.md)
- DO fail open except for security; DO sandbox agent-run code; DO put credentials in a secret store.
- DON'T rely on the model to self-police; DON'T run agent code on app servers; DON'T put creds in prompts.

## Hand off to
`reliability-and-failure` · `observability-and-ops` (audit trail).

## Evidence
`references/gap-closed-synthesis.md` (Mastra input/output processors; fail-open-except-security; sandbox isolation) ·
`references/book-code.md` (guardrails architecture; Chris Bakke injection) · `references/skill-evidence-map.md` (Orkes RBAC + secrets).
