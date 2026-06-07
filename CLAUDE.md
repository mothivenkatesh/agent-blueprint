# agent-builder — pack operating manual (CLAUDE.md)

This file is the shared context every skill in `agent-builder` inherits. It is the
distilled judgment from reading, end to end: the Orkes Conductor blog (165 posts),
"Principles of Building AI Agents" 3rd ed (Sam Bhagwat / Mastra, full book), and the
Mastra blog + agent-memory research (199 posts). Evidence maps live in `references/`.

## What this pack does

Turns a PM's idea into a **shippable Agentic AI PRD**. It does NOT build the agent.
18 skills in three layers: **Gates** (decide before you spec) → **Sections** (write +
pressure-test each PRD block) → **Spine** (assemble + critique). Each skill writes one
part of the document, forces the right decision, and cites the corpus for its defaults.

The pack exists because a generic PRD template omits the five things that make an agent
PRD an *agent* PRD: an **eval plan**, **autonomy/HITL boundaries**, a **memory strategy**,
a **failure premortem**, and a **learning loop**. Those five are the product.

---

## Prime directives (every skill obeys these)

**DO**
- **Default to the least autonomy that works.** One LLM step inside a deterministic
  workflow beats an autonomous agent until proven otherwise. ("AI reads, the workflow
  acts; the AI can be wrong, the workflow never is.")
- **Make every requirement falsifiable** and give it a trace ID (REQ-xx). If you can't
  test it, rewrite it.
- **No eval = no PRD.** `/can-we-eval-it` is a hard kill-gate. A PRD with no measurable
  acceptance criteria is not done.
- **Cite the corpus for non-obvious defaults** (model IDs, token thresholds, retry
  policy). Defaults without a source are vibes.
- **Lead each section with the decision, then the rationale**, then the requirements.
- **Treat memory + eval + learning-loop as one trio** — that trio is what "self-learning"
  actually means. Ship all three or drop the claim.
- **Budget cost and latency explicitly.** Every agent has unit economics.

**DON'T**
- **Don't write code.** This pack specs agents; it does not implement them. Snippets only
  to illustrate an interface contract.
- **Don't recommend an autonomous agent** when a workflow with one LLM step suffices.
- **Don't let an LLM emit a raw numeric score** — have it output structured data, then a
  deterministic function computes the number.
- **Don't claim "reliable" or "self-learning"** without the eval, reliability, and
  learning-loop sections filled.
- **Don't hard-code one model/provider.** Always a fallback + routing posture.
- **Don't ship stale model strings.** Date every snapshot; this field moves monthly.
- **Don't bloat a SKILL.md.** When-to-use + method in the skill; heavy detail in
  `references/`. Progressive disclosure is mandatory.

---

## PRD house style (the document the pack produces)

Sections, in order. Skills that own each are in brackets.
1. Problem, goal, non-goals, users/jobs `[/worth-an-agent]`
2. Why an agent + autonomy level + build mode `[/agent-vs-workflow]`
3. Agent type & topology (Reasoning/Operational + category) `[/agent-type]`
4. Agent architecture / component blueprint `[/agent-architecture]`
5. Capabilities, scope & decomposition `[/scope-and-topology]`
6. Tools, integrations & data access `[/tool-spec]`
7. Memory & context strategy `[/memory-spec]`
8. **Success metrics & eval plan** `[/eval-plan]`
9. **Autonomy boundaries & HITL** `[/hitl-and-autonomy]`
10. Trust, safety, security & compliance `[/safety-and-guardrails]`
11. **Reliability, latency & failure handling** `[/reliability-and-failure]`
12. Model strategy & unit economics `[/model-and-cost]`
13. Model access & gateway `[/model-gateway]`
14. Observability, ops, rollout & governance `[/observability-and-ops]`
15. **Self-improvement / learning loop** `[/learning-loop]`
16. Risks, dependencies, open questions `[all]`

Rules: requirement IDs + MoSCoW + acceptance criteria per requirement; evidence
citations inline; an open-questions list is mandatory (never fake certainty). Pairs with
`cf-product-ops` for the requirement-ID + critique machinery.

---

## The 18 skills — context + do's & don'ts

### Spine

**`/agent-prd`** — orchestrator. Intake the idea, run the gates, drive the section
skills, assemble the doc with requirement IDs and depth control.
- DO: run the three gates first and stop if any kills; thread each section's output into the next; keep an open-questions log.
- DON'T: don't generate sections the gates haven't cleared; don't invent facts to fill a section — flag a gap instead.

**`/agent-prd-review`** — critic. Score a draft agent PRD against the agentic rubric.
- DO: check all 13 sections exist; verify every claim is falsifiable; reject if no eval plan, no HITL boundary, or no failure premortem.
- DON'T: don't pass a PRD that says "reliable/self-learning" without the trio; don't soften a missing-eval finding.

### Gates (decide before you spec)

**`/worth-an-agent`** — is an agent the right tool at all?
- DO: rank options cheapest-first (no-AI script → workflow + one LLM step → agent); demand a measurable problem + baseline; require a one-line "why an agent, not a workflow."
- DON'T: don't approve an agent for a deterministic task; don't let "use AI" be the goal; don't skip ROI.
- Anchor: Orkes "40% of agentic projects scrapped by 2027"; book autonomy levels; "can I orchestrate this instead?"

**`/agent-vs-workflow`** — autonomy level + build mode.
- DO: place the use case on the spectrum (decider-node → control-flow-owner); choose code-first agent vs durable workflow engine vs hybrid; apply the rule "reach for a durable engine when it calls external APIs, runs hours/days, or must outlive a restart."
- DON'T: don't default to "autonomous agent" for hype; don't pick a durable engine for a 2-second sync task; don't equate multi-agent with A2A (niche: ~20:1 MCP-vs-A2A search).
- Anchor: book ch4/ch12; Orkes scaling pillars; Temporal/Conductor.

**`/can-we-eval-it`** — measurability kill-gate.
- DO: force a definition of "good" + at least one measurable acceptance criterion; name the eval type (task-completion, faithfulness, tool-calling, multi-turn).
- DON'T: don't pass on "we'll figure eval out later"; don't accept unfalsifiable success like "delight users."
- Anchor: book "evals are just tests"; Mastra scorers.

### Sections

**`/agent-type`** — production type classifier (runs early).
- DO: pick Reasoning vs Operational first; reuse a standard category from the 15-type taxonomy; pick the simplest topology.
- DON'T: invent a bespoke type; default to multi-agent; skip the cognitive-class call (it sets eval/cost/guardrail intensity).
- Anchor: Lyzr Reasoning/Operational 15-type taxonomy; Antigma agent-org + sub-agents.

**`/agent-architecture`** — component blueprint (the parts list, above tool/memory specs).
- DO: enumerate every slot (authored context, learned memory, tools, MCP, skills, sub-agents, model+gateway, permissions, surface); separate authored rules from learned memory; state the deployment surface.
- DON'T: collapse context/memory/tools into one box; leave the model-access layer implicit; decide topology here.
- Anchor: Antigma ante anatomy (AGENTS.md vs MEMORY.md, tools/MCP/skills/sub-agents, protocol/storage, surfaces).

**`/model-gateway`** — model-access control plane (augments model-and-cost).
- DO: scope virtual keys with hard budgets; define overrun + unreachable-backend behavior; attribute spend; allow BYOK.
- DON'T: ship raw provider keys to the runtime; assume one provider's wire format; bury this inside "pick a model".
- Anchor: Antigma antix (routing, virtual keys + budgets, BYOK, fail-closed, spend attribution).

**`/scope-and-topology`** — capabilities + agent shape.
- DO: write a capability map and explicit non-goals; start single-agent, justify supervisor/hierarchical only when a single agent provably can't; one job per agent.
- DON'T: don't design a multi-agent org chart before one agent works; don't leave non-goals blank.
- Anchor: book multi-agent grid ("start with the simplest version first"); Orkes Intake/Verify/Decision specialists.

**`/tool-spec`** — tools, integrations, data access.
- DO: list the tools first (write them on a napkin before anything else); define I/O schemas; mark side-effecting tools idempotent; prefer MCP; put schema constraints in the property `description`.
- DON'T: don't dump a whole corpus into context instead of giving search tools; don't ship a tool without an I/O schema; don't trust a third-party MCP server like it's safe.
- Anchor: book "designing your tools is the most important step" (Alana agent); Mastra tool-compat (15%→3%); Orkes idempotency/TryStart.

**`/memory-spec`** — memory & context strategy.
- DO: pick a type deliberately — working memory = personalization, semantic recall (RAG) = factual recall, observational memory = tool-heavy/long sessions, or none; set retention + freshness; append, never wholesale-replace.
- DON'T: don't use working memory for long-term recall; don't add a vector DB when observational text memory or no memory suffices; don't drop timestamps / "today's date."
- Anchor: Mastra observational-memory + use-rag-for-agent-memory research; book ch7/ch19 ("build an agent first, RAG as fallback").

**`/eval-plan`** ★ — success metrics + eval.
- DO: define a golden dataset (hand-curate + synthetic + mine production logs); a rubric where the LLM emits structured data and code computes the score; acceptance thresholds; offline + online evals; a regression gate that fails the build on a drop.
- DON'T: don't let an LLM emit a raw 0-1 number; don't judge with the same model family as the agent; don't ship without a regression gate.
- Anchor: Mastra scorers / datasets / experiments / compareExperiments; book ch27.

**`/hitl-and-autonomy`** ★ — autonomy boundaries + approval.
- DO: place the human gate where the irreversible risk fires, as late as is still safe; distinguish approval (yes/no, before the act) from suspension (clarify mid-act); default to tool-level approval, tighten to agent-level only when the whole op is risky.
- DON'T: don't gate everything (alert fatigue); don't auto-approve money-movement or destructive actions; don't place approval where no state has run yet (design smell).
- Anchor: Mastra HITL posts (trust spectrum, approval-vs-suspension); Orkes HUMAN/WAIT + signal API; book agent middleware.

**`/safety-and-guardrails`** — trust, safety, security, compliance.
- DO: spec input + output guardrails (prompt-injection, PII, jailbreak, toxicity); fail open by default, fail closed for security; RBAC + secrets + sandbox isolation + spend caps; an audit trail.
- DON'T: don't rely on the model to self-police; don't run agent-generated code on app servers (sandbox it); don't put credentials in prompts.
- Anchor: Mastra input/output processors; book ch9 (Chris Bakke injection); Orkes RBAC + secrets + status-listener audit trail.

**`/reliability-and-failure`** ★ — NFRs + failure premortem.
- DO: set the 4-layer model (task retry → task timeout → workflow timeout → compensation/failure-workflow) + rate limits + idempotency; a latency budget; write a premortem of failure modes with mitigations; degrade predictably.
- DON'T: don't retry without idempotency (duplicate side effects); don't stretch timeouts for long tasks (use async-poll); don't assume the happy path.
- Anchor: Orkes durability cluster + saga/compensation; book deployment; Mastra model fallback + "fail open."

**`/model-and-cost`** — model strategy + unit economics.
- DO: tier models (cheap/fast for classification, strong for reasoning/tools, Claude for tool-heavy steps); define a fallback chain with per-model retries; set a token + latency budget and cost-per-task.
- DON'T: don't hard-code one provider; don't ignore unit economics (the "$500k token bill"); don't assume a prompt is portable across models.
- Anchor: book provider table (Mar 2026) + token-cost chapter; Mastra model-router/fallback; tool-call reliability ranking (Claude > GPT > Gemini > others).

**`/observability-and-ops`** — observability, ops, rollout, governance, versioning.
- DO: spec tracing (spans + token/cost at trace level), metrics (latency, cost, scores, errors), drift detection, an on-call runbook, dev→prod promotion, versioning, and success/rollback criteria.
- DON'T: don't ship without tracing (agents regress while returning 200 OK); don't track only infra metrics — track decision quality; don't change a live looping workflow without versioning.
- Anchor: Mastra 3-pillars / AI tracing; book ch26; Orkes versioning + RBAC + monitoring.

**`/learning-loop`** ★ — self-improvement plan.
- DO: specify how the agent improves over time — production traces → datasets-from-prod → re-eval → regression gate; state what is automated vs human-reviewed and the review cadence.
- DON'T: don't claim "self-learning" without this section; don't promise fully-automatic retraining — be honest that the prompt/tool rewrite is still human-in-the-loop today (the frontier).
- Anchor: Mastra ai-ops ("Continued Learning in CI/CD") + datasets-from-traces; book ch33.

---

## How the skills chain

`/worth-an-agent` → `/agent-vs-workflow` → `/can-we-eval-it` (gates; stop if any kills)
→ `/agent-type` then `/agent-architecture` (classify + blueprint) → the remaining section
skills (`/model-gateway` runs with `/model-and-cost`; `/eval-plan` is required because the eval
section gates the others) → `/agent-prd` assembles → `/agent-prd-review` audits.

Hard dependency: you cannot complete §6 (Success/eval) without `/eval-plan`, and
`/can-we-eval-it` will not pass without a rubric. Memory, eval, and learning-loop are the
self-learning trio — if any is missing, `/agent-prd-review` flags the PRD as not
self-learning.

## Freshness rule

Model IDs, API names, and pricing in `references/` are dated snapshots. Re-verify before
quoting them in a live PRD. A skill that recommends a dead model string is worse than no
skill. Bump the plugin version when references are refreshed.

## References (the moat)

- `references/skill-evidence-map.md` — Orkes reliability/HITL/governance canon
- `references/gap-closed-synthesis.md` — Mastra memory + eval + self-improve canon
- `references/book-code.md` — verbatim code recovered from the Principles ebook
- `references/antigma-lyzr-architecture.md` — Antigma ante architecture + Lyzr agent-type taxonomy
Every skill cites these instead of restating them.
