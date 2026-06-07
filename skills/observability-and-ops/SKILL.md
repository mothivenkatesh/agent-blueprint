---
name: observability-and-ops
description: >
  Specify an agent's observability, operations, rollout, and governance. Use when planning
  tracing/metrics/logs, drift detection, on-call, dev→prod promotion, versioning, RBAC, or
  rollback criteria for an agent. Writes PRD §11 in the agent-builder pack.
allowed-tools: Read, Write, Edit
---

# observability-and-ops  (PRD §11)

Read `../../CLAUDE.md` first.

## When to use
Before launch. Agents regress while still returning 200 OK — you cannot operate what you can't see.

## Method
1. Tracing: spans for every agent/tool/model call, with token count + cost at the trace level,
   input/output inspection. Use the OpenTelemetry standard.
2. Metrics: latency percentiles, cost, eval scores, error rate per agent/tool/workflow.
3. Logs: searchable, linked to trace IDs.
4. Drift detection: watch decision quality + failure rate over time, not just infra metrics;
   alert on behavioral drift, not only thresholds.
5. Rollout & governance: dev→prod promotion path, versioning (never change a live looping flow
   without it), RBAC, progressive delivery, and explicit success + rollback criteria + a runbook.

## Output (PRD §11)
Tracing/metrics/logging plan + drift alerts + rollout plan (environments, versioning, progressive
delivery) + success/rollback criteria + on-call runbook.

## Do / Don't (full list in CLAUDE.md)
- DO ship tracing from day one; DO track decision quality; DO write rollback criteria.
- DON'T track only infra metrics; DON'T change a live workflow without versioning.

## Hand off to
`learning-loop` (observability feeds it) · `agent-prd` (assemble).

## Evidence
`references/gap-closed-synthesis.md` (Mastra 3-pillars / AI tracing / DuckDB-ClickHouse) ·
`references/skill-evidence-map.md` (Orkes audit + versioning + RBAC; book ch26 tracing).
