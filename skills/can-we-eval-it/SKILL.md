---
name: can-we-eval-it
description: >
  Hard gate: can the agent's success be measured before you commit to building it? Use when
  defining acceptance criteria for an agent, asking "how will we know it works", or before
  green-lighting an agent build. If you cannot produce a rubric, the answer is: don't build.
  Gate 3 of 3 in the agent-builder pack; feeds eval-plan.
allowed-tools: Read, Write, Edit
---

# can-we-eval-it  (gate 3 of 3 — hard kill-gate)

Read `../../CLAUDE.md` first. Core rule: **no eval = no PRD.**

## When to use
Before any build commitment. "Evals are just tests" — if you can't test it, you can't ship it.

## Method
1. Write the success definition in ONE falsifiable sentence (not "delight users").
2. Name the eval type(s) that apply: task-completion, faithfulness/hallucination, tool-calling,
   classification/labeling, multi-turn, latency/cost.
3. Feasibility check:
   - Is there ground truth, or can an LLM-judge + rubric score it?
   - Can you get at least ONE realistic test case today?
4. Decision: if you cannot define success AND sketch a rubric → KILL. Send back to
   `worth-an-agent` or reframe the problem. Do not proceed to build.

## Output
Measurable success statement + eval type(s) + a go/no-go. On go, pass the rubric sketch to `eval-plan`.

## Do / Don't (full list in CLAUDE.md)
- DO force a measurable acceptance criterion now.
- DON'T pass on "we'll figure eval out later"; DON'T accept unfalsifiable success.

## Hand off to
`eval-plan` (builds the full harness).

## Evidence
`references/gap-closed-synthesis.md` (book "evals are just tests" ch27; Mastra scorers; eval-type taxonomy).
