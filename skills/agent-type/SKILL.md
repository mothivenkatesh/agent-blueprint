---
name: agent-type
description: >
  Classify the agent's production type so the rest of the spec inherits the right defaults. Use
  when naming what kind of agent this is, deciding "is this a reasoning or an operational
  agent", picking a production agent category (research, support, reporting, monitoring, coding,
  data-transformation, etc.), or choosing a multi-agent topology. Writes the "Agent type &
  topology" section in the agent-blueprint pack; runs early, feeds eval, cost, and guardrails.
allowed-tools: Read, Write, Edit
---

# agent-type  (PRD §3a — runs early)

Read `../../CLAUDE.md` first.

## When to use
Right after you've decided to build an agent (`worth-an-agent`, `agent-vs-workflow`). Naming the
type sets the intensity of eval, cost, and guardrails downstream.

## Method
1. **Cognitive class (pick one):**
   - **Reasoning** — thinks in real time, open-ended (deep research, negotiation, data analysis,
     evaluation, coding, conversational, recommendation). → invest in eval + critique.
   - **Operational** — reliably executes repeatable workflows with speed, safeguards, and
     **predictable cost** (reporting, follow-up, scheduling, monitoring/maintenance, data
     transformation, knowledge search, document analysis, content generation). → invest in
     cost ceilings + safeguards.
2. **Named category:** pick the closest standard category (above) and copy its example
   obligations into scope, instead of inventing a bespoke type.
3. **Topology:** single agent → orchestrator + sub-agents → multi-agent (`Independent`,
   `Decentralized`, `Centralized Iterative`, `Hybrid Iterative`). Pick the simplest that meets
   the quality bar. (Deep decomposition itself lives in `scope-and-topology`.)
4. **Surface + trigger:** interactive / headless-CI / served-daemon / chat-gateway, and who or
   what triggers it (user, cron, webhook, mention).

## Output (PRD §3a)
Cognitive class + named category + topology + surface/trigger, with one line on how this sets
eval/cost/guardrail intensity.

## Do / Don't (full list in CLAUDE.md)
- DO make the Reasoning-vs-Operational call first; DO reuse a standard category; DO pick the simplest topology.
- DON'T invent a bespoke type when a standard fits; DON'T default to multi-agent; DON'T skip the class call.

## Hand off to
`scope-and-topology` (decompose) · `eval-plan` / `model-and-cost` / `safety-and-guardrails` (inherit intensity).

## Evidence
`references/antigma-lyzr-architecture.md` (Lyzr Reasoning/Operational 15-type taxonomy; Antigma agent-org + sub-agent patterns).
