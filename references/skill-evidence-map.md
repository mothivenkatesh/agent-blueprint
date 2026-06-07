# Orkes Blog → agent-foundry Skill Evidence Map

Built from a word-by-word read of all 165 Orkes blog posts (scraped locally to `raw_full/`,
228,542 words). 8 deep-read reader agents covered the 79 AI/RELIABILITY/ORCH-CORE posts in
full; 2 triage agents classified all 86 OTHER posts (18 turned out RELEVANT).

## Headline finding: evidence splits the 22 skills into 3 tiers

Orkes' corpus richly documents RELIABILITY + ORCHESTRATION + HITL + BUILD. It partially
documents MEMORY/EVAL. It barely touches SELF-IMPROVEMENT. So:

- **Tier A (distill + wrap Orkes):** commodity — anyone can build these from the blogs.
- **Tier B (supplement Orkes):** half-covered; needs Agentspan/Prompt Studio docs.
- **Tier C (original IP):** the gap Orkes does NOT fill = agent-foundry's defensible value.

This empirically confirms the project steer: the self-learning trio (memory + eval + self-improve)
and the judgment Council are where the differentiation lives. Tier A is table stakes.

---

## TIER A — Strongly grounded (13 skills)

| Skill | Strength | Key source posts | Load-bearing mechanisms (exact) |
|---|---|---|---|
| agent-or-workflow | STRONG | agentic-ai-explained, scaling, what-are-agentic-workflows, both ticket-triage posts, llm-text-vs-chat, orchestration-vs-choreography, control-flow-operators | agent-vs-workflow table + 6 criteria; "one step thinks, rest deterministic"; Orkes def "agentic = any step uses an LLM for its decision-making"; orchestration vs choreography; **two build modes: Agentspan (code agent) vs Conductor (workflow graph)** |
| decompose-the-goal | STRONG | scaling (Intake/Verify/Decision), prompt-engineering, operators-parallelism, fraud (modular sub-wf) | sub-workflow/worker decomposition; chain vs parallel; FORK_JOIN / DYNAMIC_FORK |
| reliability-harness | VERY STRONG (deepest seam) | durability+resilience cluster (9), idempotency, timeouts-retries, task/workflow-level-resilience, saga, compensation, long-running, orchestrating-long-running-apis, Tesla-powerwall, all-about-cli | 4-layer model (task retry → task timeout → wf timeout → failureWorkflow) + rate limits; exact fields + defaults; TryStart idempotency; saga/compensation; HTTP_POLL+terminationCondition; LLM task implicit 60s/60s |
| hitl-gate | VERY STRONG | human-in-the-loop, operators-loops-waits-human-tasks, customer-success, insurance, loan, sending-signals, webhooks, conductor-skills(signal-wait) | HUMAN task + User Form (JSON-Schema draft-07) + assignment_completion_strategy; WAIT vs HUMAN; signal APIs (POST /tasks/{wf}/{ref}/{status}); webhook `matches`; Agentspan @tool(approval_required=True) |
| hitl-policy | STRONG | human-in-the-loop, scaling pillar 2, future-of-agentic-boat, insurance/loan/fraud thresholds, customer-success rules | confidence-threshold routing; risk tiers (>$25k, >0.0 prob); SLA + escalation + default-action design; where to place the human |
| trust-safety-gate | STRONG | scaling (guardrails), rbac, conductor-has-secrets, doc-classification (PII), UCP (runaway spend), why-orchestration | RBAC (users/roles/tags env:prod, least privilege, audit), secrets `${workflow.secrets.*}`, PII obfuscation, spend guardrails, "do not invent values" |
| tool-designer | STRONG | conductor-skills, using-system-tasks, why-use-system-tasks, workers, MCP posts, embeddings, why-apps-need-durable-exec | @tool + docstrings; system vs worker vs inline trade-off table; idempotent/immutable/atomic tool design; MCP wrapping; secret injection; DYNAMIC task = runtime tool selection |
| prompt-decomposer | STRONG | prompt-engineering-in-agentic-workflows, llm-text-vs-chat | chain vs parallel; `${var}` output-chaining; structured JSON output contract |
| prompt-lab | VERY STRONG | test-ai-prompts (Prompt Studio), prompt-engineering-in-practice, guide-to-prompt-engineering | isolation + `${var}` parameterization + multi-model comparison; checklist: 10+ inputs incl adversarial, 2+ models, one-word-at-a-time; temperature sweep; 5W1H |
| observability-board | STRONG | durable-execution, monitoring-prometheus-grafana, running-a-billion, opsgenie-alerting, debugging-distributed-systems, DPG-payment-hub | Prometheus metrics (latency p50/95/99, success/failure rate, throughput); pending-task-queue-depth = autoscale signal; Query-Processor over Search API → page Opsgenie on cron; Status Listeners → Kafka → audit tables |
| governance-promote | STRONG | rbac, workflow-versioning, conductor-has-secrets, gpt-5.2 (env gating), differences-oss-vs-orkes | version pin/latest, restart --use-latest, running-instance POST /upgrade; conservative migration + dual-read worker; RBAC tags; secrets; OSS→Orkes promotion checklist |
| model-cost-fit | MEDIUM-STRONG | gpt-5.2 (model catalog, reasoning-effort/xhigh, fallbacks), prompt-engineering-in-practice (model-as-ringfence), build-ai-app (multi-provider), running-a-billion (capacity #s) | model-as-swappable-component; cost-routing cheap/simple vs powerful/complex; fallbacks; temperature/topP; ~210 wf/s/node sizing |
| ship-with-claude | VERY STRONG | conductor-skills, how-to-build-with-claude-code, conductor-mcp-server, ai-orchestration-meetup | SKILL.md anatomy + allowed-tools; /plugin install commands; CLI-first + conductor_api.py fallback; MCP wiring; OSS-local vs hosted Developer Edition creds |

## TIER B — Partially grounded (4 skills; supplement from Agentspan/Prompt Studio docs)

| Skill | Strength | What the corpus gives | What's missing |
|---|---|---|---|
| agent-memory | PARTIAL (build only) | RAG (index/search workflows), vector DBs (Pinecone/Weaviate/Postgres/Mongo), LLM embedding tasks, Chat `messages` array, ghost-chat `initialize_agent_memory`, SetVariable, GPT-5.2 Compaction | No episodic/cross-run learning memory; "schedule re-index" is the only freshness story |
| can-we-eval-it | PARTIAL | benchmark/gold-standard (practice post), versioning executable verifier, python-sdk unit-test+replay, KPIs (cycle time/throughput/success rate) | No agent-output eval methodology; "inspectable architecture" is the only built-in check |
| eval-loop | PARTIAL | systematic testing at sample size, workflow unit-test + replay, regression verifier, serde generated-tests-as-regression, metrics dashboards | No closed eval→improve loop; no LLM-as-judge; no golden-set harness |
| rubric-builder | PARTIAL | 5W1H rubric (practice post); score+confidence+reason outputs (insurance/loan/fraud) | No weighting/anchor/kill-criteria methodology (this is why rubric-builder is its own skill) |

## TIER C — The GAP = agent-foundry's original IP (3+ skills, near-zero Orkes evidence)

| Skill | Strength | The only in-corpus anchors |
|---|---|---|
| self-improve | NEAR-ZERO | fraud "use review decisions to retrain your models" + confidence; embeddings "detect anomalies from past patterns"; versioning "evolve without breaking in-flight" |
| memory-strategy (Council judgment) | NEAR-ZERO | build-mechanics exist; no "when/what to remember / retention" judgment anywhere |
| failure-premortem | WEAK-PARTIAL | saga/compensation scenarios, idempotency crash-retry & owner-conflict, ChatGPT-codegen failure catalog, timeout→retry-storm cascade (no premortem METHOD) |
| is-it-worth-an-agent | MEDIUM (judgment) | 40%-scrapped stat, "can I orchestrate this instead?" (serde 5d→1hr), start-with-POC, "agentic = LLM-in-the-loop", gray-area-task heuristic |

---

## Reframes the full read forces on the design

1. **Default to "one LLM step in a deterministic workflow," not an autonomous agent.** The single
   most-repeated doctrine across the corpus: "AI reads, Conductor acts / the AI can be wrong, the
   workflow logic never is / agentic workflows are a safer alternative to AI agents." `is-it-worth-an-agent`
   and `agent-or-workflow` should bias the PM toward the smallest amount of autonomy that works.

2. **Two build modes, one spine.** Agentspan (Python `Agent/@tool/AgentRuntime/max_turns/EventType`,
   `agentspan server start` :6767) for building a single durable agent; Conductor (JSON/SDK task graph)
   for orchestrating multi-step/multi-agent systems. "Build the agent in Agentspan, orchestrate
   everything else in Conductor." `agent-or-workflow` gets a 3rd fork: agent-as-code / workflow-as-graph / hybrid.

3. **Reliability is the corpus's crown jewel and it's all config.** A PM can get production-grade
   reliability without code: the 4-layer model + idempotency + saga/compensation + async-poll for long
   tasks. `reliability-harness` can ship literal JSON templates (see appendix).

4. **The audit-trail primitive is real and maps to the Relay wedge.** DPG-payment-hub: custom
   Workflow/Task StatusListeners stream every state change to Kafka → audit tables, on a money-movement
   saga. This is HITL-evidence + audit implemented in Conductor. Consider a dedicated `audit-trail` angle
   inside `trust-safety-gate`/`observability-board`.

5. **agent-foundry's defensible value is Tier C, not Tier A.** Anyone can wrap Orkes' reliability/HITL
   docs. The judgment Council (is-it-worth-an-agent, can-we-eval-it, rubric-builder, failure-premortem)
   and the self-learning trio (cross-run agent-memory, eval-loop, self-improve) are exactly what 165
   Orkes posts do NOT teach. Build the pack to LEAD with those.

---

## Appendix: load-bearing exact strings (for writing the SKILLs)

**Conductor task/operator types:** SIMPLE, HTTP, HTTP_POLL, INLINE, JSON_JQ_TRANSFORM, EVENT,
WAIT, WAIT_FOR_WEBHOOK, SWITCH, DYNAMIC, SET_VARIABLE, TERMINATE, DO_WHILE, FORK_JOIN, JOIN,
DYNAMIC_FORK, SUB_WORKFLOW, START_WORKFLOW, HUMAN; AI tasks: LLM_TEXT_COMPLETE, LLM_CHAT_COMPLETE,
LLM_GENERATE_EMBEDDINGS, LLM_STORE_EMBEDDINGS, LLM_GET_EMBEDDINGS, LLM_INDEX_TEXT, LLM_INDEX_DOCUMENT,
LLM_GET_DOCUMENTS, LLM_SEARCH_INDEX, GET_DOCUMENT.

**Retry (defaults 3/60s/FIXED/1):** retryCount, retryLogic (FIXED | LINEAR_BACKOFF | EXPONENTIAL_BACKOFF),
retryDelaySeconds, backoffScaleFactor. Linear = delay×factor×attempt; Exp = delay×(factor^attempt).

**Timeout (defaults resp 600 / total 3600 / poll 3600 / TIME_OUT_WF):** timeoutSeconds, pollTimeoutSeconds,
responseTimeoutSeconds, timeoutPolicy (RETRY | TIME_OUT_WF | ALERT_ONLY). Workflow: timeoutSeconds (0=off),
timeoutPolicy, failureWorkflow. Rate limit: rateLimitPerFrequency, rateLimitFrequencyInSeconds.
System-task implicit: HTTP 30/60, **LLM 60/60**, Inline 4s, Business Rule 10/120.

**Idempotency:** TryStart against durable store keyed on business identity; cache + replay stored result.
**Long tasks:** non-blocking HTTP (return requestId) + external status store + HTTP_POLL (pollingInterval,
pollingStrategy:FIXED, terminationCondition). **Compensation:** failureWorkflow receives failed wf ID + tasks.

**Agentspan:** `pip install agentspan` (+anthropic); `from agentspan.agents import Agent, AgentRuntime, tool, EventType, run`;
`Agent(name, model="provider/model", tools=[...], instructions, max_turns)`; model strings
anthropic/claude-sonnet-4-6, anthropic/claude-sonnet-4-20250514, openai/gpt-4o; `@tool` / `@tool(approval_required=True)`;
`runtime.run(agent,input)` or `runtime.start(agent,prompt)`→`handle.stream()`; EventType.TOOL_CALL/TOOL_RESULT/DONE;
`agentspan server start` → http://localhost:6767.

**HITL:** HUMAN task → User Form (JSON-Schema draft-07 + templateUI) + assignment_completion_strategy; WAITING state;
resume via form submit or signal API. WAIT = pause for duration or external signal/webhook.

**Governance:** RBAC users/roles/permissions + Applications/Groups + Tags (env:prod); secrets `${workflow.secrets.*}`;
versioning: start --version N / unpinned→latest; restart --use-latest; running-instance POST /api/workflow/{id}/upgrade.

**Observability:** Prometheus (latency p50/95/99, success/failure, throughput); pending-task-queue-depth = autoscale;
Query-Processor over Search API → Opsgenie on cron; Workflow/Task StatusListeners → Kafka → audit.

**ship-with-claude:** `/plugin marketplace add conductor-oss/conductor-skills`; `/plugin install conductor@conductor-skills`;
CLI v0.1.3; `conductor workflow create/start/retry`, `conductor task signal`; CLI-first + scripts/conductor_api.py fallback;
env CONDUCTOR_SERVER_URL / _AUTH_KEY / _AUTH_SECRET; hosted https://developer.orkescloud.com/api.

## Hidden gems (from OTHER triage — don't skip these when building)
- **DPG-payment-hub** — status-listeners→Kafka audit trail on money-movement saga (Relay-relevant).
- **debugging-distributed-systems** — failure-class taxonomy + distributed tracing + fail-at-iteration-17/429 example.
- **all-about-the-conductor-oss-and-orkes-cli** — best retry-vs-restart, idempotent token, bulk-retry source.
- **monitoring-prometheus-grafana / running-a-billion / opsgenie-alerting** — the observability-board toolkit.
- **Tesla-powerwall** (Feb 2026, most recent) — cleanest idempotent sense→decide→act loop to clone.
- **whats-new-python-sdk** — workflow unit-testing + replay (only eval hooks in the corpus).
- **reduce-reuse-recycle** — DYNAMIC task = runtime tool selection.
