---
name: eval-plan
description: >
  Write the success-metrics and evaluation section of an agent PRD. Use when designing how to
  measure or score an agent, building a golden dataset, setting up LLM-as-judge, defining
  acceptance thresholds, or wiring a regression gate for an agent. The differentiator section
  most agent PRDs skip. Runs after can-we-eval-it.
allowed-tools: Read, Write, Edit
---

# eval-plan  ★ (PRD §6)

Read `../../CLAUDE.md` first.

## When to use
To turn `can-we-eval-it`'s go into an actual, shippable eval plan.

## Method
1. Golden dataset: combine hand-curated + synthetic + mined-from-production cases. Define the
   item shape (input + optional ground truth) with a schema; add a case for every bug you find.
2. Scorers:
   - Code-based (exact / string / rule) for objective checks.
   - LLM-as-judge for subjective: the LLM emits STRUCTURED data (verdicts, extracted claims),
     and a deterministic function computes the 0-1. Never let the LLM emit the raw number.
     Pick a judge from a different model family than the agent.
3. Rubric: criteria + weights + acceptance threshold (the pass bar). Mark kill-criteria (a
   single binary fail that zeroes the score, e.g. policy violation, money moved unapproved).
4. Offline (fixed dataset, pre-deploy, catches regressions) + online (sample production traffic).
5. Regression gate: CI runs experiments, pins the dataset version, fails the build if the score
   drops vs the baseline.

## Output (PRD §6)
Dataset plan + scorer list + rubric (criteria/weights/thresholds + kill-criteria) +
offline+online setup + the regression gate. Acceptance criteria become testable REQ-ids.

## Do / Don't (full list in CLAUDE.md)
- DO make the LLM emit structure → code scores it; DO ship a regression gate.
- DON'T let the LLM emit a raw 0-1; DON'T judge with the same model family; DON'T ship without thresholds.

## Hand off to
`agent-prd` (assemble) · `observability-and-ops` (online scoring) · `learning-loop` (mine traces → dataset).

## Evidence
`references/gap-closed-synthesis.md` (Mastra scorers / datasets / experiments / compareExperiments; book ch27) ·
`references/book-code.md` (createFaithfulnessScorer; LLM-as-judge caveats).
