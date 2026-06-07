---
name: agent-architecture
description: >
  Lay out the full component blueprint of an agent before writing detailed requirements. Use
  when designing an agent's architecture, deciding its parts (context, memory, tools, MCP,
  skills, sub-agents, model gateway, permissions), drawing a component/data-flow diagram, or
  asking "what are the pieces of this agent and how do they connect". Writes the "Agent
  architecture / component blueprint" section in the agent-builder pack.
allowed-tools: Read, Write, Edit
---

# agent-architecture  (PRD §3b)

Read `../../CLAUDE.md` first. This is the assembly/parts-list view — it sits *above*
`tool-spec` and `memory-spec`, not in place of them.

## When to use
After the agent's type and topology are set, to enumerate the concrete components and who owns each.

## Method
Enumerate every anatomy slot and assign an owner + store:
1. **Context — authored rules** (system prompt + standing rules the agent must enforce; name the file/store).
2. **Context — inline inputs** (per-request file/RAG/@-mention injection).
3. **Memory — learned** (what persists across sessions, scoped how; name the store). Keep this
   separate from authored rules — different lifecycles.
4. **Tools** (built-in vs MCP vs custom — defer contracts to `tool-spec`).
5. **Skills** (reusable instruction packs the agent can load).
6. **Sub-agents** (specialized children spawned by the main agent; their prompt/tools/model).
7. **Model + gateway** (defer routing/keys to `model-gateway`).
8. **Permissions / approvals** (which tool calls are allow / ask / deny).
9. **Deployment surface** (interactive / headless / served / gateway-bot) — it changes HITL +
   streaming requirements, so state it here.
Then draw the component diagram and label the data flow (who calls the model, where tool
results go, where context is injected).

## Output (PRD §3b)
A labeled component blueprint (each slot + its owner/store) + a component/data-flow diagram +
the deployment surface.

## Do / Don't (full list in CLAUDE.md)
- DO enumerate every slot; DO separate authored context from learned memory; DO state the deployment surface.
- DON'T collapse context/memory/tools into one box; DON'T leave the model-access layer implicit; DON'T decide topology here (that's `scope-and-topology`).

## Hand off to
`tool-spec` · `memory-spec` · `model-gateway` (the components this blueprint names get specified there).

## Evidence
`references/antigma-lyzr-architecture.md` (the ante component anatomy: AGENTS.md vs MEMORY.md, tools/MCP/skills/sub-agents, protocol + storage, surfaces).
