---
name: agent-vs-workflow
description: >
  Choose the autonomy level and build mode for an agent product. Use when deciding "agent or
  workflow or hybrid", picking how autonomous an agent should be, or choosing a build
  architecture (code-first agent framework vs durable workflow engine vs hybrid). Gate 2 of 3
  in the agent-blueprint pack; writes the "why an agent + approach" section.
allowed-tools: Read, Write, Edit
---

# agent-vs-workflow  (gate 2 of 3)

Read `../../CLAUDE.md` first.

## When to use
After `worth-an-agent` clears, to fix the autonomy level and build mode before specifying capabilities.

## Method
1. Place the use case on the autonomy spectrum; pick the LOWEST that works:
   - L0 decider-node: LLM makes a choice inside a fixed workflow graph
   - L1 agent: memory + tools + retry on failure
   - L2 high-autonomy: plans, splits subtasks, manages a queue, runs parallel sub-agents, self-corrects
2. Choose the build mode:
   - Code-first agent framework — agent owns control flow; fast iteration; type-safe (Mastra-style)
   - Durable workflow engine — retries, scheduling, survives restart, HITL-at-scale (Conductor / Temporal)
   - Hybrid — build the agent in a framework, embed it as a step in a durable workflow
   - Rule: reach for the durable engine when it calls external APIs, runs hours/days, or must
     outlive a worker restart. Otherwise prefer code-first for speed.
3. Note single vs multi-agent (full topology lives in `scope-and-topology`).

## Output (PRD §2)
Autonomy level + build mode + one-paragraph justification citing the rule.

## Do / Don't (full list in CLAUDE.md)
- DO default to the least autonomy + simplest build mode that works.
- DON'T pick "autonomous agent" for hype; DON'T use a durable engine for a 2-second sync task;
  DON'T equate multi-agent with A2A (niche, ~20:1 MCP-vs-A2A).

## Hand off to
`can-we-eval-it` · `scope-and-topology`.

## Evidence
`references/gap-closed-synthesis.md` (book ch4/12 autonomy levels; the two build modes) ·
`references/skill-evidence-map.md` (Orkes "one step thinks, rest deterministic"; durable-engine rule).
