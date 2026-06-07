---
name: model-and-cost
description: >
  Specify an agent's model strategy and unit economics. Use when choosing models, designing a
  fallback chain, setting a token/latency budget, estimating cost-per-task, or deciding which
  steps get a cheap vs a strong model. Writes PRD §10 in the agent-builder pack.
allowed-tools: Read, Write, Edit
---

# model-and-cost  (PRD §10)

Read `../../CLAUDE.md` first.

## When to use
Once capabilities, tools, and memory are known (they drive token volume and model choice).

## Method
1. Tier the models by step: fast/cheap for classification/extraction (e.g. a nano/flash model),
   strong for reasoning and tool-heavy steps. Note: tool-calling reliability is provider-ranked
   (Claude > GPT > Gemini > others); prefer Claude for tool-heavy/agentic steps.
2. Define a fallback chain with per-model retries (e.g. primary → secondary → tertiary) so a
   provider outage doesn't take the agent down. Use model routing so a swap is one line.
3. Set a token + latency budget and estimate cost-per-task. Sanity-check the "$500k token bill"
   risk: tokens-cost vs revenue-per-task.
4. State which model strings are used (and that they are a dated snapshot — re-verify).

## Output (PRD §10)
Model-per-step table + fallback chain + token/latency budget + cost-per-task estimate.

## Do / Don't (full list in CLAUDE.md)
- DO tier models by task; DO define a fallback chain; DO compute unit economics.
- DON'T hard-code one provider; DON'T ignore the token bill; DON'T assume prompt portability across models.

## Hand off to
`observability-and-ops` (track real cost) · `agent-prd` (assemble).

## Evidence
`references/book-code.md` (Mar-2026 provider table; "$500k token bill"; make-it-work-right-cheap) ·
`references/gap-closed-synthesis.md` (Mastra model-router/fallback; tool-call reliability ranking).
