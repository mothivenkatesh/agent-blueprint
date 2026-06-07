# agent-foundry evidence — Mastra + Principles book close the Tier C gap

Sources now read end-to-end for the pack:
- **Orkes Conductor**: 165 blog posts (228,542 words) — reliability/orchestration/HITL/governance.
- **"Principles of Building AI Agents" 3rd ed (Sam Bhagwat / Mastra)**: 135pp, read in full — the judgment + agent-building principles layer.
- **Mastra blog + research**: 199 posts (120,787 words) — agent-first framework depth, esp. MEMORY + EVALS.

The headline: after Orkes, 7 skills were under-evidenced (Tier B/C: agent-memory, memory-strategy, can-we-eval-it, eval-loop, rubric-builder, self-improve, failure-premortem). **Mastra + the book ground all of them.** The pack is now fully sourced.

## The gap, closed (per skill)

| Skill | Was (Orkes only) | Now (Mastra + book) | Key source |
|---|---|---|---|
| agent-memory | PARTIAL (RAG build only) | **STRONG** — 3 memory types + Observational Memory spec (observer→reflector, 30k/40k thresholds, two-block context, three-date model, emoji log-levels, text-not-graph) + RAG config (resourceId/threadId, recent+semantic+surrounding, topK) | research-observational-memory, observational-memory, agent-memory-guide, book ch7 |
| memory-strategy | NEAR-ZERO | **STRONG** — 3-way decision: working-memory=personalization / semantic-recall=factual-recall (tune topK 2→20 = 63%→80%) / OM=tool-heavy+cacheable, no vector DB; "build agent first, RAG as fallback"; append-not-replace rule | research-use-rag-for-agent-memory, book ch19 |
| can-we-eval-it | PARTIAL | **STRONG** — "evals are just tests"; eval-type taxonomy (relevancy/faithfulness/hallucination/tool-calling/multi-turn/task-completion); ground-truth + Zod/JSON schema gate | book ch27, ai-engineering, introducing-datasets |
| eval-loop | PARTIAL | **STRONG** — Scorer API 4-step pipeline; datasets + experiments + compareExperiments as a CI **fail-build-on-regression** gate; offline vs online; run-on-every-change; LongMemEval | mastra-scorers, introducing-datasets, mastra-experiments, book ch27 |
| rubric-builder | PARTIAL | **STRONG** — the load-bearing pattern: **LLM emits structured data, deterministic `generateScore` makes the number** (never let the LLM emit the score); clone-a-scorer (shadcn-style) then tweak; judge from a different model family | mastra-scorers, introducing-cloneable-scorers, book ch27 |
| self-improve | NEAR-ZERO | **MEDIUM-STRONG** — concrete path: traces → datasets-from-production-traces (announced) → SME annotation → synthetic distribution testing (re-run prod queries 5-30x) → "Continued Learning in CI/CD"; OM dogfooding loop; scores as first-class storage domain | ai-ops, introducing-datasets, research-observational-memory, book ch33 |
| failure-premortem | WEAK | **MEDIUM** — silent failure modes (context rot, lossy compaction, stateless sessions); fail-open-except-security; abort-on-corruption; the model×constraint test grid | anatomy-of-a-coding-agent, building-fast-reliable-input-processors |

## Skills further enriched (already Tier A, now sharper)

- **hitl-policy / hitl-gate** — the two-axis model: WHEN (trust spectrum; approval=gatekeeping vs suspension=clarification; tool-level vs agent-level) and WHERE (handoff graph; gate at the irreversible-risk point, as late as still safe). Mechanics: `requireApproval`/`requireToolApproval`/`suspend()`/`resumeStream`/`approveToolCall`/auto-resume. (hitl-where-to-put-approval, human-in-the-loop-when-to-use-agent-approval, tool-approval, building-multi-user-multi-channel-agents)
- **trust-safety-gate** — input/output processors (Moderation, PromptInjection, PIIDetector, SystemPromptScrubber); **fail-open by default, fail-closed for security**; sandbox blast-radius isolation (Daytona/E2B/Blaxel, networkBlockAll). (building-fast-reliable-input-processors, introducing-output-processors, introducing-remote-sandboxes)
- **model-cost-fit** — model-router (600+ models, magic strings), fallback chains w/ per-model retries; **tool-calling reliability is provider-ranked: Claude > GPT > Gemini > DeepSeek/Llama** (Gemini silently ignores schema constraints); fast/small models for classification (gpt-4.1-nano, Gemini Flash-Lite). (model-router, model-fallback, mcp-tool-compatibility-layer)
- **observability-board** — 3 pillars (traces+metrics+logs), AI Tracing (OTel base, token-at-trace-level, Braintrust/Langfuse exporters), auto-instrumentation, DuckDB/ClickHouse columnar store, sampling.rate online scoring. (introducing-studio-metrics, aitracing, mastra-scorers)
- **ship-with-claude** — "**MCP gives capabilities; skills teach how to use them**"; 4-block knowledge stack (docs→skills→MCP docs server→embedded docs); Skills Specification + CLAUDE.md/AGENTS.md; progressive disclosure; skills are living docs. (introducing-mastra-skills, how-to-structure-projects-for-ai-agents-and-llms)
- **agent-or-workflow** — confirmed **two build modes**: code-first agent framework (Mastra: agent owns control flow, TS types, fast iteration) vs durable workflow engine (Orkes/Temporal: retries, scheduling, survives restart). Rule: "reach for the durable engine when workflows call external APIs, stretch over hours/days, or must outlive a worker restart." Autonomy levels: decider-node-in-workflow (low) → control-flow-owner (high). (vNext-workflows, introducing-temporal-workflows, choosing-a-js-agent-framework, book ch4/ch12)

## Canonical specs to hard-code when writing the SKILLs

**Observational Memory (the agent-memory centerpiece):** two context blocks (observations + raw messages); Observer agent compresses raw→dated observations at ~30k-40k tokens; Reflector agent restructures/GCs observations at the higher threshold; text not structured objects; three-date model (observation / referenced / relative date); emoji log levels 🔴/🟡/🟢; 3-6x compression text, 5-40x tool-heavy; prompt-cache friendly (append-only prefix); SOTA LongMemEval 84-95%. Default observe model gemini-2.5-flash.

**RAG-for-memory:** working memory = personalization (template, append-not-replace via updateReason/searchString); semantic recall = vector store of messages, topK is the accuracy/latency lever (2=63%, 20=80%); fix timestamps + "today's date" anchor + group-by-date formatting; backends pgvector/Pinecone/Chroma/LibSQL; adaptive IVFFlat/HNSW over fixed; rebuild index at >20% new data or recall drift.

**Eval recipe:** createScorer 4 steps (preprocess→analyze→generateScore[required]→generateReason); LLM outputs structured data, code computes the number; datasets (versioned, Zod/JSON schema, build from CSV/JSON/prod-traces); experiments = run dataset through target + score; compareExperiments(baseline, new) → fail CI build on any regression; offline (pre-deploy) + online (sampling.rate). "Evals are just tests."

**HITL:** approval (yes/no gate, before the act) vs suspension (clarification, mid-act); tool-level requireApproval default, agent-level requireToolApproval when whole op risky; place the gate where irreversible risk fires, as late as safe; auto-resume only for low-risk conversational + needs memory+same-thread.

**Model:** Claude for tool-heavy/agentic steps (highest tool-call reliability); fast/small for classification; fallback chain (e.g. GPT-5 → Claude Sonnet → Claude Opus) with per-model retries; put schema constraints in the property `description` (models honor it there).

## The three-source spine for agent-foundry

1. **Judgment layer (the Council)** — grounded by the Principles book (autonomy levels, "is this worth an agent", tool-design-first, memory-type choice, "evals are just tests") + Mastra's HITL/prototype-playbook judgment posts.
2. **Build mode A — code-first agent** — Mastra (Agent/@tool/memory/scorers/processors). Best for agent-owned control flow, fast iteration.
3. **Build mode B — durable workflow engine** — Orkes Conductor / Temporal. Best for retries, long-running, HITL-at-scale, audit/governance.

agent-foundry is the PM-facing layer that decides between them and wires reliability + the self-learning trio (memory + eval-loop + self-improve) across both. Self-learning is no longer the empty gap — it is memory (OM/RAG) + eval (scorers+datasets+experiments) + the trace→dataset→regenerate-eval→regression-gate loop, with the only still-frontier piece being automated prompt/tool rewrite (agent-foundry's value-add).

## Open follow-up (not yet deep-read)
- `announcing-agent-signals.md` — flagged by triage as a novel context-engineering primitive (addressable agent loop: reactive / state / notification signals; prompt-cache-friendly working memory). Worth a deep read before finalizing the agent-memory + self-improve skills.
