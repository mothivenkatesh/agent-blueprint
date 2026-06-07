---
name: worth-an-agent
description: >
  Decide whether an AI agent is even the right tool, before writing an agent PRD. Use when a
  PM is scoping an agentic product, asks "should we build an agent for X", is choosing between
  an agent / a workflow / a script / buying a tool, or is starting an Agentic AI PRD. Ranks
  solutions cheapest-first and kills agent ideas that should be a deterministic workflow.
  Gate 1 of 3 in the agent-builder pack.
allowed-tools: Read, Write, Edit
---

# worth-an-agent  (gate 1 of 3)

Read `../../CLAUDE.md` first — its prime directives and do's & don'ts apply.

## When to use
At the very start of any agent spec, or whenever someone assumes "let's build an agent"
without proving an agent is the cheapest tool that works.

## Method
1. State the problem in one line + today's baseline (time / cost / error rate).
2. Climb the solution ladder, cheapest first; pick the LOWEST rung that meets the goal:
   - L0 do nothing
   - L1 deterministic script (rules, no LLM)
   - L2 workflow with ONE LLM step ("AI reads, the workflow acts")
   - L3 workflow with multiple LLM steps
   - L4 single autonomous agent (tools in a loop)
   - L5 multi-agent system
3. Kill questions:
   - Is the task deterministic / rule-expressible? → stop at L1-L2, not an agent.
   - Is there a measurable definition of success? → if no, hand to `can-we-eval-it` (likely kill).
   - ROI: does the value beat build + run cost? (Tokens are real; mind the "$500k bill" risk.)
   - Build vs buy: does an existing tool already do this?
4. Verdict: agent / not-an-agent, the chosen rung, non-goals, the baseline metric.

## Output (seeds PRD §1-2)
- Problem, users/jobs, baseline metric
- Verdict + chosen rung + one-line "why an agent, not a workflow"
- Non-goals

## Do / Don't (full list in CLAUDE.md)
- DO rank cheapest-first; demand a measurable problem; require the why-an-agent line.
- DON'T approve an agent for a deterministic task; DON'T let "use AI" be the goal.

## Hand off to
`agent-vs-workflow` (on pass) · `can-we-eval-it` (to confirm measurability).

## Evidence
`references/skill-evidence-map.md` (Orkes "40% of agentic projects scrapped by 2027"; "can I
orchestrate this instead?", 5-day→<1hr) · `references/gap-closed-synthesis.md` (book autonomy levels).
