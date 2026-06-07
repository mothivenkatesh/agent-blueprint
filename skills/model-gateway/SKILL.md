---
name: model-gateway
description: >
  Spec the model-access control plane for a production agent. Use when designing provider
  routing, virtual keys with budget caps, BYOK, spend attribution, multi-provider fallback, or
  fail-closed behavior for an agent's LLM access. Augments model-and-cost; writes the "Model
  access & gateway" section in the agent-blueprint pack.
allowed-tools: Read, Write, Edit
---

# model-gateway  (PRD §10b — augments model-and-cost)

Read `../../CLAUDE.md` first. `model-and-cost` picks the models + estimates cost; this skill
specs how the agent *gets* model access in production as a governed control plane.

## When to use
For any production agent, especially multi-provider, multi-tenant, or budget-sensitive ones.

## Method
1. **Routing:** single-provider vs gateway-fronted multi-provider. If gateway, list the wire
   protocols to normalize on one base URL (OpenAI / Anthropic / Gemini shapes).
2. **Budget governance:** per-key budget + rate caps (day / month / lifetime) and the rejection
   behavior on overrun (e.g. hard 402). Caps from `model-and-cost` become enforceable here.
3. **Failure posture:** fail-closed vs fail-open if the gateway/billing backend is unreachable;
   per-turn transport fallback (e.g. WS → HTTP).
4. **Keys & tenancy:** scoped **virtual keys** to the runtime — never raw provider keys; allow
   BYOK where needed.
5. **Spend attribution:** which org / member / key / prompt is billed (feeds observability).

## Output (PRD §10b)
Routing posture + per-key budget/rate caps + overrun behavior + fail-closed/open decision +
key/tenancy model + spend-attribution plan.

## Do / Don't (full list in CLAUDE.md)
- DO scope virtual keys with hard budgets; DO define the overrun + unreachable-backend behavior; DO attribute spend.
- DON'T ship raw provider keys to the agent runtime; DON'T assume one provider's wire format; DON'T bury this inside "pick a model".

## Hand off to
`model-and-cost` (cost caps) · `observability-and-ops` (spend attribution) · `safety-and-guardrails` (key governance).

## Evidence
`references/antigma-lyzr-architecture.md` (Antigma antix: routing, virtual keys + budgets, BYOK, fail-closed, spend attribution).
