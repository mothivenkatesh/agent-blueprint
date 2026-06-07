---
name: tool-spec
description: >
  Specify an agent's tools, integrations, and data access. Use when listing what an agent can
  call, designing tool input/output schemas, deciding MCP vs custom tools, or planning
  read/write access to external systems. "Designing your tools is the most important step."
  Writes PRD §4 in the agent-blueprint pack.
allowed-tools: Read, Write, Edit
---

# tool-spec  (PRD §4)

Read `../../CLAUDE.md` first.

## When to use
Right after scope. The tool list is the single highest-leverage design decision for an agent.

## Method
1. List the tools FIRST (the "napkin" rule) — think like an analyst: what queries/operations
   would a human expert run? Each becomes a tool.
2. For each tool define: id, a description of WHAT it does AND WHEN to call it, an input schema,
   an output schema. Use semantic names (`refundOrder`, not `doStuff`).
3. Mark every side-effecting tool (charge, send, delete, write) as needing idempotency
   (a stable key from a business identity) — handled in reliability-and-failure.
4. Source: prefer an existing MCP server over building an integration; treat third-party MCP
   servers with the same trust as any external API (vet them).
5. State read vs write scope per integration and the auth method (secrets, never hard-coded).

## Output (PRD §4)
Tool table (id · does/when · input · output · side-effecting? · source) + integration + data-access list.

## Do / Don't (full list in CLAUDE.md)
- DO write the tool list before anything else; DO give every tool an I/O schema; DO prefer MCP.
- DON'T dump a whole corpus into context instead of giving search tools; DON'T trust third-party MCP blindly.

## Hand off to
`memory-spec` · `safety-and-guardrails` (auth/secrets) · `reliability-and-failure` (idempotency).

## Evidence
`references/book-code.md` (createTool + best practices; "designing your tools is the most important step", Alana agent) ·
`references/gap-closed-synthesis.md` (Mastra MCP, tool-compat 15%→3%, constraints-in-description).
