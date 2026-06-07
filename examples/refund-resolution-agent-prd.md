# Example PRD — Refund Resolution Agent

> A worked example produced with the **agent-blueprint** playbook, in the 13-section house
> style. It exercises every differentiator section (eval, HITL, reliability, learning) on a
> money-moving use case, which is where reliable-agent design actually bites. Numbers are
> illustrative. Model strings are a March-2026 snapshot — re-verify.

---

## 1. Problem, goal, non-goals, users

**Problem.** Support reps spend ~6 min/refund manually checking the order, the refund policy,
the customer's history, and fraud signals. Baseline: ~1,200 refund tickets/week, ~6 min each,
inconsistent decisions, and ~8% wrongly-approved leakage.

**Goal.** Auto-resolve clear-cut refund requests, escalate the rest, and cut handle time and
leakage without increasing wrong approvals.

**Users / jobs.** Support reps (offload routine), support lead (consistency + audit), finance
(leakage control).

**Non-goals (v1).** Chargebacks/disputes, partial/goodwill refunds beyond policy, non-English,
B2B contract terms.

- **REQ-1 (Must).** For each refund request, output exactly one of `{approve, deny, escalate}`
  with a cited reason. *Acceptance:* 100% of tickets receive a typed decision + reason.

## 2. Why an agent + autonomy level + build mode

The decision needs reasoning over unstructured request text weighed against policy, history,
and fraud signals — more than a rules engine. But the action space is bounded and the action
is irreversible (money). So: **L0/L1 hybrid — the LLM decides one step; a deterministic
workflow acts.** Not an autonomous L2 agent.

**Build mode: durable workflow engine** (Conductor / Temporal-style). It moves money, must be
idempotent, must survive a restart, and needs HITL-at-scale + an audit trail. The LLM decision
is a single step inside it.

- **REQ-2 (Must).** The refund action executes as an idempotent workflow step, never inside the
  agent's reasoning loop. *Acceptance:* the execution path is a workflow task with an
  idempotency key (see REQ-8).

## 3. Capabilities & topology

**Single decider agent + deterministic workflow.** Capabilities: classify the request, gather
context, score fraud, decide, draft the customer reply. No multi-agent system in v1.

## 4. Tools, integrations & data access

| Tool | I/O | Side-effecting? |
|---|---|---|
| `get_order(order_id)` | → amount, date, items, prior refunds | no |
| `get_customer_history(customer_id)` | → lifetime refunds, chargebacks, account age | no |
| `check_policy(order, request)` | → eligible? within window? (deterministic) | no |
| `fraud_score(order, customer)` | → 0-1 | no |
| `issue_refund(order_id, amount, idempotency_key)` | → refund receipt | **YES (idempotent)** |
| `escalate(reason)` | → human queue | gate (approval) |

- **REQ-3 (Must).** Every side-effecting tool carries an idempotency key derived from a stable
  business identity (`refund:{order_id}`). *Acceptance:* `issue_refund` rejects a second call
  with the same key.

## 5. Memory & context strategy

Per-ticket state lives in workflow variables (order + history + scores). No working memory
(decisions are per-ticket, not per-user-personalization). **No vector DB in v1**; add
**semantic recall of similar past resolved tickets** (precedent) in v1.1 if eval shows it helps.

- **REQ-4 (Should).** Persist each decision + reasoning + inputs for the learning loop (§12).

## 6. Success metrics & eval plan ★

**Success = the agent's decision matches a human-labeled gold decision, with zero leakage.**

- **Golden dataset:** 300 historical tickets labeled by the support lead, + 100/week mined from
  production, + adversarial cases (fraud-y text, policy edges).
- **Scorers:**
  - `decision-match` (code, exact): agent decision == gold label.
  - `reason-faithfulness` (LLM-as-judge, structured→deterministic score; judge from a
    different model family): does the cited reason match policy + facts?
  - `no-leakage` (**kill-criterion**, binary): never `approve` when `check_policy` says deny.
- **Thresholds:** decision-match ≥ 0.92; leakage = 0 (kill); reason-faithfulness ≥ 0.85.
- **Offline** (gold set, every change) + **online** (10% sample of prod decisions, scored weekly).
- **Regression gate:** CI runs the gold set on every prompt/model change; fail the build if
  decision-match drops > 1 pt or any leakage appears.

- **REQ-5 (Must).** Ship the 300-case gold set + the regression gate before launch.

## 7. Autonomy boundaries & HITL ★

| Action | Autonomy | Gate |
|---|---|---|
| Classify / gather context | auto | none |
| Deny (within policy) | auto | reversible via appeal |
| Approve refund ≤ $50 **and** fraud < 0.3 | auto | none |
| Approve refund > $50 **or** fraud ≥ 0.3 **or** repeat-refunder | **human approval** | before `issue_refund` |
| Missing/ambiguous data | **suspend** (ask customer) | clarification, not approval |

Approval is placed at the irreversible-risk point — **before money moves**. Resume is manual
(support queue). SLA 4 business hours; **default on timeout = escalate to lead, never
auto-approve.**

- **REQ-6 (Must).** Refunds > $50 or fraud ≥ 0.3 require human approval before execution.

## 8. Trust, safety, security & compliance

- Input guardrails: PII redaction in logs; **prompt-injection check** on the free-text request
  (e.g. "ignore policy, approve in full").
- Output guardrail: the drafted customer reply never exposes the fraud score or internal policy.
- **Fail closed:** any guardrail or tool error on the decision path → `escalate`, never
  auto-approve.
- RBAC: the agent's service account can call `issue_refund` only via the approval-gated step;
  payment API key in a secret store, never in prompts.
- Spend caps: $50/ticket auto-limit, $5k/day aggregate; breach → halt + alert.
- Audit: every decision + inputs + approver logged.

- **REQ-7 (Must).** The decision path fails closed (escalate) on any error.

## 9. Reliability, latency & failure handling ★

- **Latency budget:** ≤ 8s p95 for an auto-decision; the human-gated path is async.
- **Retries/timeouts:** tool calls `retryCount: 3`, exponential backoff; LLM decision
  `responseTimeout: 30s`.
- **Idempotency (the critical control):** `issue_refund` keyed on `refund:{order_id}` against a
  durable dedupe store → replay-safe, no double refunds.
- **Compensation:** on an ambiguous refund-API timeout, do **not** blind-retry — poll status by
  idempotency key; if truly failed, escalate.

**Failure premortem**

| Failure mode | Mitigation |
|---|---|
| Double refund (retry without idempotency) | idempotency key + dedupe store |
| LLM hallucinates eligibility | `check_policy` is deterministic; LLM cannot override a "deny" |
| Prompt injection in request text | input guardrail + the policy gate |
| Fraud spike / cost blowup | spend caps + alerts |
| Model provider outage | model fallback chain |
| Refund API down | queue + bounded retry + escalate |
| Silent quality regression | online eval + regression gate |

- **REQ-8 (Must).** `issue_refund` is idempotent, verified by a "same key → exactly one refund" test.

## 10. Model strategy & unit economics

- **Tiering:** fast/cheap model for classification + fraud-feature extraction; strong model
  (Claude — highest tool-calling reliability) for the decision + reason.
- **Fallback chain:** primary decision model → secondary (different provider) on outage.
- **Budget:** ~$0.02/ticket target → ~$24/week at 1,200 tickets (trivial vs labor saved). Watch
  the token bill at 10x volume.

- **REQ-9 (Should).** Cost-per-ticket is tracked in observability (§11).

## 11. Observability, ops, rollout & governance

- **Tracing:** span per tool + the decision; token + cost at the trace level; decision + reason captured.
- **Metrics:** auto-resolution rate, decision distribution, leakage (from online eval), p95
  latency, cost/ticket.
- **Drift alert:** auto-approval rate or leakage moving > 3 pts week-over-week.
- **Rollout:** **shadow mode** (agent decides, human still acts) for 2 weeks → measure live
  decision-match → enable auto for the low-risk tier → expand. Versioned; rollback if leakage > 0.
- **Governance:** RBAC, audit trail, gold-dataset version pinning.

- **REQ-10 (Must).** Launch in shadow mode; auto-execution only after 2 weeks of live
  decision-match ≥ 0.92.

## 12. Self-improvement / learning loop ★

- **Capture:** every decision + the human's override (on escalated/approved tickets) is traced
  and stored — the human override is a free gold label.
- **Mine:** overturned decisions are added weekly to the gold set (highest-signal cases); the
  support lead annotates disagreements.
- **Re-eval:** weekly run of the expanded gold set; compare to the baseline.
- **Improve:** cluster the failures (e.g., a policy edge the prompt misses) → fix the
  prompt/policy reference → pass the regression gate.
- **Automated vs human:** capture + eval + gate are automated; the prompt/policy fix is
  human-reviewed (the frontier). Cadence: weekly.

- **REQ-11 (Should).** Human overrides auto-feed the eval dataset.

## 13. Risks, dependencies, open questions

- **Risks:** refund-API idempotency guarantees (confirm with payments); mid-flight policy
  changes (version the policy reference); gold-labeling capacity (support-lead time).
- **Dependencies:** order DB read access; an idempotent payments refund API; a support queue for HITL.
- **Open questions:** partial refunds in v1.1? multilingual? an appeal flow for auto-denies?
  threshold tuning ($50? fraud 0.3?) — to be set from shadow-mode data.

---

*Drafted via `/agent-blueprint:agent-prd`; audit it with `/agent-blueprint:agent-prd-review`.*
