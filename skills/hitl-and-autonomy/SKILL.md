---
name: hitl-and-autonomy
description: >
  Design the human-in-the-loop and autonomy boundaries of an agent. Use when deciding where a
  human must approve, what the agent may do on its own, approval vs clarification, or how to
  gate risky / irreversible actions (payments, deletes, sends, transfers). The differentiator
  section that keeps an agent trustworthy. Writes PRD §7.
allowed-tools: Read, Write, Edit
---

# hitl-and-autonomy  ★ (PRD §7)

Read `../../CLAUDE.md` first.

## When to use
Whenever the agent can take real-world actions, or a stakeholder asks "what can it do without us?"

## Method
1. List the agent's actions; place each on the trust spectrum: harmless (search, read) →
   consequential (charge, delete, send, transfer, post).
2. For each consequential action choose:
   - Approval = yes/no gate BEFORE the act (for risk).
   - Suspension = pause to gather missing input, then continue (for clarity, not risk).
3. Placement: put the gate where the irreversible risk fires, as late as is still safe.
   Default tool-level approval; escalate to agent-level only if the whole operation is risky.
4. Resume: manual (button / dashboard, for high-risk) vs auto-resume (low-risk conversational;
   requires memory + same thread).
5. Add SLA + escalation + a safe default action on timeout.

## Output (PRD §7)
An autonomy-boundary table (action → autonomy level → approval/suspension → resume path) +
escalation/SLA rules.

## Do / Don't (full list in CLAUDE.md)
- DO gate at the irreversible-risk point, as late as safe; DO distinguish approval vs suspension.
- DON'T gate everything (alert fatigue); DON'T auto-approve money-movement/destructive actions;
  DON'T place approval where no state has run yet (design smell).

## Hand off to
`safety-and-guardrails` · `agent-prd` (assemble).

## Evidence
`references/gap-closed-synthesis.md` (Mastra trust spectrum, approval-vs-suspension, where-to-place) ·
`references/skill-evidence-map.md` (Orkes HUMAN/WAIT + signal API; book agent middleware).
