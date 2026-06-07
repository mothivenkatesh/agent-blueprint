# Antigma "ante" architecture + Lyzr agent-type taxonomy

Distilled from a full read of the Antigma `ante` docs (ante.run, 43 pages) and Lyzr's
"Agent Types in Production". Source corpus: `antigma-research/raw/`. These ground the three
architecture skills: `agent-architecture`, `agent-type`, `model-gateway`.

## 1. The agent component anatomy (ante)

The parts a PM should enumerate when blueprinting an agent. Each is a distinct layer with its
own lifecycle and owner — do not collapse them into one "knowledge" box.

| Component | Role |
|---|---|
| **Context — authored rules** | Persistent instructions the agent must enforce, loaded every session (ante: `AGENTS.md`, global + project). Authored, stable. |
| **Context — inline inputs** | Per-request file/dir/RAG injection (ante: `@path` mentions). |
| **Memory — learned** | Generated, per-project observations that change over time (ante: `MEMORY.md`, first N lines injected). Distinct from authored rules. |
| **Tools** | "The agent's hands": Read/Write/Edit/Bash/WebFetch/Browser/etc. Built-in vs MCP vs custom. |
| **MCP servers** | External tool surface as subprocesses; tools callable like built-ins (`mcp__<server>__<tool>`). |
| **Skills** | Portable instruction packs (`SKILL.md`, Agent Skills format), invoked on demand. |
| **Sub-agents** | Specialized children the main agent spawns (own prompt/tools/model), return a result. |
| **Model + gateway** | Provider-agnostic model access; optionally fronted by a gateway (see §3). |
| **Permissions / approvals** | First-match-wins allow/ask/deny per tool call; HITL gate (accept / accept-for-session / skip / abort). |
| **Protocol + storage** | Typed message contract (Ops/Events) + on-disk state (sessions, memory, config) → enables persistence/resume + observability. |
| **Deployment surface** | interactive (TUI) · headless (CI) · served (daemon for editors/web) · gateway-bot (Slack/Discord, isolated session per thread). Surface changes HITL + streaming needs. |

**Key distinction:** authored context (rules to enforce) ≠ learned memory (observations that
change). Name the store for each.

## 2. Architecture / topology patterns (ante)

1. **Single agent** — one loop + built-in tools.
2. **Orchestrator + sub-agents** — main agent delegates to specialized children; the common
   production default.
3. **Multi-agent collaboration (agent-org)** — 4 named topologies:
   - `Independent` — run in parallel, aggregate results.
   - `Decentralized` — peers exchange rounds → consensus.
   - `Centralized Iterative` — orchestrator + quality gates.
   - `Hybrid Iterative` — orchestrator + peer refinement.
4. **Gateway-fronted** — any agent points at a model gateway for routing/keys/budgets.

## 3. Model gateway / control plane (ante "antix") — net-new

Model *access* is an architecture component, not just "pick a model":
- One base URL normalizes multiple provider wire protocols (OpenAI / Anthropic / Gemini shapes).
- **Virtual keys** with hard budget + rate caps (reject on overrun, e.g. HTTP 402).
- **BYOK** + **spend attribution** (org / member / key / prompt).
- **Fail-closed by default** if billing/upstream is unreachable; per-turn transport fallback.
- Scoped virtual keys to the runtime — never raw provider keys.

## 4. Agent types in production (Lyzr) — the cognitive-class taxonomy

Two classes, 15 named types.
- **Reasoning agents** — "think in real time": Deep Research, Negotiation, Data Analysis,
  Evaluation, Coding, Conversational, Recommendation.
- **Operational agents** — "reliably execute repetitive workflows with speed, safeguards, and
  predictable cost": Reporting, Follow-up, Calendar/Scheduling, Monitoring/Maintenance, Data
  Transformation, Knowledge Search, Document Analysis, Content Generation.

The class is the single classifier that sets downstream intensity: **Reasoning → invest in
eval/critique; Operational → invest in predictable cost + safeguards.**

## 5. The PM's production-agent spec = three orthogonal choices

`{ cognitive class (Reasoning | Operational) + named category }`
× `{ topology (single | orchestrator+sub-agents | agent-org pattern) }`
× `{ deployment surface (interactive | headless | served | gateway-bot) }`

## 6. Net-new vs the Orkes/Mastra-grounded pack

- **Model gateway as a first-class component** (routing + virtual-key budgets + BYOK +
  fail-closed) — the pack previously treated the model as a choice + cost line only.
- **`agent-org` named multi-agent topologies** — sharper than a generic "decompose the work".
- **Reasoning-vs-Operational production taxonomy** — a vendor-neutral classifier + a 15-category
  menu so PMs don't invent types.
- **Authored-context vs learned-memory split + protocol/storage layer** — architecture surface
  the pack's `memory-spec` did not cover.
