---
name: agent-prd
description: >
  Draft a complete Agentic AI PRD from a product idea. Use when a PM says "write a PRD for
  this agent", wants to turn an agent idea into a spec, or needs the full agentic product
  document. The orchestrator: runs the gates, drives the section-writers, and assembles a
  traceable PRD. The entry point of the agent-blueprint pack.
allowed-tools: Read, Write, Edit
---

# agent-prd  (orchestrator)

Read `../../CLAUDE.md` first — it defines the prime directives, the 13-section house style,
and the per-skill do's & don'ts you will apply throughout.

## When to use
The front door. Use to produce a full Agentic AI PRD, or to resume one mid-way.

## Method
1. Intake — ask the 5 framing questions: the problem + users; the perfect run end-to-end;
   what would make a user or auditor angry; the non-negotiables; the stakes (reversible vs not).
2. Gates (stop if any kills): `worth-an-agent` → `agent-vs-workflow` → `can-we-eval-it`.
3. Sections (thread each output into the next), in CLAUDE.md order:
   `agent-type` → `agent-architecture` → `scope-and-topology` → `tool-spec` → `memory-spec` →
   `eval-plan` → `hitl-and-autonomy` → `safety-and-guardrails` → `reliability-and-failure` →
   `model-and-cost` → `model-gateway` → `observability-and-ops` → `learning-loop`. Use whichever
   section skills are installed;
   flag any not yet available rather than skipping the section silently.
4. Assemble the 13-section PRD: every requirement gets a REQ-id + MoSCoW + acceptance
   criteria; cite `references/` for non-obvious defaults; keep a live open-questions list.
5. Hand to `agent-prd-review` for the audit.

## Output
A complete Agentic AI PRD (the 13-section house-style doc) + an open-questions list.

## Do / Don't (full list in CLAUDE.md)
- DO run the gates first and stop on a kill; DO flag gaps instead of inventing facts.
- DON'T generate sections the gates haven't cleared; DON'T claim "reliable / self-learning"
  without the eval, reliability, and learning-loop sections.

## Pairs with
`cf-product-ops` (requirement-ID + critique machinery) · `agent-prd-review` (final audit).

## Evidence
All of `references/`: `skill-evidence-map.md` · `gap-closed-synthesis.md` · `book-code.md`.
