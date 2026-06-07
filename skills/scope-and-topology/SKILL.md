---
name: scope-and-topology
description: >
  Define an agent's capabilities, non-goals, and agent topology (single vs supervisor vs
  multi-agent). Use when scoping what an agent will and won't do, deciding whether one agent
  or several, or designing a supervisor/sub-agent structure. Writes PRD §3 in the agent-blueprint pack.
allowed-tools: Read, Write, Edit
---

# scope-and-topology  (PRD §3)

Read `../../CLAUDE.md` first.

## When to use
After the gates clear, to bound what the agent does and how many agents it takes.

## Method
1. Write a capability map: the jobs-to-be-done the agent must cover, each as a verb-phrase.
2. Write explicit non-goals (what it will NOT do in v1). An empty non-goals list is a red flag.
3. Choose topology, simplest first:
   - Single agent (default) — start here; one job, one loop.
   - Supervisor + sub-agents (agents-as-tools) — only when distinct roles + clear handoffs justify it.
   - Hierarchical / network — only at real scale ("a hierarchy is just a supervisor of supervisors").
4. For each agent, state its one job, its tools, its memory, and its hand-offs.

## Output (PRD §3)
Capability map + non-goals + topology diagram-in-words + per-agent one-job statement.

## Do / Don't (full list in CLAUDE.md)
- DO start single-agent and justify multi; DO give each agent exactly one job.
- DON'T design a multi-agent org chart before a single agent works; DON'T leave non-goals blank.

## Hand off to
`tool-spec` · `memory-spec`.

## Evidence
`references/book-code.md` (multi-agent pattern grid: Single/Network/Supervisor/Hierarchical/Custom;
"start with the simplest version first") · `references/skill-evidence-map.md` (Orkes specialist decomposition).
