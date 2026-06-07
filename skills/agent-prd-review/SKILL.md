---
name: agent-prd-review
description: >
  Audit an agent / Agentic-AI PRD against the reliability rubric and return a scorecard. Use when
  a PM has a draft agent PRD and wants it reviewed, asks "what's missing from this spec", or wants
  to pressure-test an agent product doc before build. Works on an existing PRD with zero setup —
  the fastest way to feel the agent-builder pack's value.
allowed-tools: Read, Write, Edit
---

# agent-prd-review  (critic / spine)

Read `../../CLAUDE.md` first — you audit against its prime directives + the 13-section house style.

## When to use
On any existing agent PRD or product spec. This is the zero-setup entry point: paste a doc, get a gap report.

## Method
1. Check completeness: are all 13 sections present? Flag every missing one.
2. Check the kill conditions (auto-fail if any is true):
   - No eval plan / no measurable acceptance criteria.
   - No human-in-the-loop boundary for consequential actions.
   - No failure premortem.
   - Claims "reliable" or "self-learning" without the eval + reliability + learning-loop trio.
3. Check quality per section: is every requirement falsifiable? Are defaults cited? Is autonomy
   bounded? Are model strings dated? Is cost budgeted?
4. Score each section (pass / weak / missing) and compute an overall verdict.
5. Output the Agent PRD Scorecard: section-by-section grades, the kill-condition results, and a
   prioritized fix list. Make it shareable.

## Output
An Agent PRD Scorecard (per-section grade + kill-condition results + ranked fixes + overall go/no-go).

## Do / Don't (full list in CLAUDE.md)
- DO reject on any kill condition; DO make every finding specific and actionable.
- DON'T pass a PRD that says "reliable/self-learning" without the trio; DON'T soften a missing-eval finding.

## Pairs with
`agent-prd` (the author) — review closes the loop on what it drafts.

## Evidence
All of `references/` — the rubric is the distilled judgment from Orkes + the Principles book + Mastra.
