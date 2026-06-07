---
name: memory-spec
description: >
  Decide an agent's memory and context strategy. Use when choosing what an agent should
  remember, picking working memory vs semantic recall (RAG) vs observational memory vs none,
  designing retention/freshness, or sizing a context window. Writes PRD §5 in the agent-blueprint pack.
allowed-tools: Read, Write, Edit
---

# memory-spec  (PRD §5)

Read `../../CLAUDE.md` first.

## When to use
Whenever the agent needs to remember anything across turns, sessions, or users.

## Method
1. Decide if it needs memory at all. Short, single-turn, stateless tasks need none.
2. Pick the type deliberately (they answer different questions):
   - Working memory = personalization (durable user facts via a template). NOT for long-term recall.
   - Semantic recall (RAG) = factual recall across sessions. Tune topK to your latency budget
     (2→63%, 20→80% on LongMemEval). Needs a vector store.
   - Observational memory = tool-heavy / long sessions. Observer compresses raw → dated
     observations (~30k token trigger); reflector garbage-collects (~40k). Text, not graphs.
     Prompt-cache friendly, no vector DB.
3. Set retention + freshness (re-index cadence) and scoping (resourceId/threadId).
4. Two easy-to-miss rules: append, never wholesale-replace memory; keep timestamps + a
   "today's date" anchor.

## Output (PRD §5)
Memory type(s) chosen + why + retention/freshness + scoping + storage backend.

## Do / Don't (full list in CLAUDE.md)
- DO match type to need; DO append not replace; DO keep dates correct.
- DON'T use working memory for long-term recall; DON'T add a vector DB when text/none suffices.

## Hand off to
`eval-plan` (memory has its own eval) · `model-and-cost` (memory drives tokens).

## Evidence
`references/gap-closed-synthesis.md` (Mastra observational-memory + use-rag-for-agent-memory research; the 3-way rule) ·
`references/book-code.md` (observationalMemory config; TokenLimiter/ToolCallFilter; RAG pipeline).
