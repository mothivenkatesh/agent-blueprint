---
name: learning-loop
description: >
  Specify how an agent improves over time — the self-learning loop. Use when planning continuous
  improvement, turning production traces into eval datasets, defining what is automated vs
  human-reviewed, or claiming an agent is "self-learning." The section that earns the word. Writes
  PRD §12 in the agent-builder pack.
allowed-tools: Read, Write, Edit
---

# learning-loop  ★ (PRD §12)

Read `../../CLAUDE.md` first. An agent is "self-learning" only with memory + eval + this loop.

## When to use
Whenever the product claims it gets better over time, or whenever it will run long enough to.

## Method
1. Capture: every production run is traced + scored online (sampling rate).
2. Mine: turn production traces into curated eval datasets (the highest-signal source) instead
   of hand-writing them; have SMEs annotate failures at the item level.
3. Re-eval: run the new cases through the eval harness; compare to baseline.
4. Improve: identify the failing cluster; fix prompts/tools/memory; re-run the regression gate.
5. Be honest about automation: state what is automated (capture, eval, regression gate) vs
   human-in-the-loop (the prompt/tool rewrite — still the frontier today). Set a review cadence.

## Output (PRD §12)
The improvement loop (capture → mine → re-eval → fix → gate) + automated-vs-human split + review cadence.

## Do / Don't (full list in CLAUDE.md)
- DO connect traces → datasets → eval → fix → gate; DO state the human-in-the-loop steps honestly.
- DON'T claim "self-learning" without this section; DON'T promise fully-automatic retraining.

## Hand off to
`agent-prd` (assemble) · pairs with `eval-plan` + `observability-and-ops` (the self-learning trio).

## Evidence
`references/gap-closed-synthesis.md` (Mastra ai-ops "Continued Learning in CI/CD" + datasets-from-traces;
OM dogfooding loop; book ch33 "the feedback loop runs through human programmers").
