# Book code appendix — recovered from the Principles ebook

Code and diagrams in "Principles of Building AI Agents" (3rd ed, Sam Bhagwat / Mastra,
March 2026) are rasterized images that text extraction skipped. These were recovered by
rendering each PDF page to PNG and reading them visually. Syntax is Mastra (TypeScript).
**Model IDs are a March-2026 snapshot — re-verify before quoting in a live PRD.**

## Providers & models (March 2026 table, p7)

| Provider | Default | Cheap/Fast | Reasoning |
|---|---|---|---|
| OpenAI (hosted) | GPT-5.4 | GPT-5 mini, GPT-5 nano | reasoning built into GPT-5.4 w/ effort controls; GPT-5.2 Thinking/Pro |
| Anthropic (hosted) | Claude Sonnet 4.6 | Claude Haiku 4.5 | Claude Opus 4.6 |
| Google Gemini (hosted) | Gemini 3 Flash | Gemini 3.1 Flash-Lite | Gemini 3.1 Pro |
| DeepSeek (OSS) | DeepSeek V3.2 | efficient by default (MoE) | DeepSeek R1 series |
| Alibaba Qwen (OSS) | Qwen 3.5 | Qwen3-30B-A3B | QwQ-32B |

Rule: "make it work, make it right, make it fast/cheap — in that order." Start with larger
models; move workloads to cheaper ones when scaling cost matters. Reasoning models: turn
`effort` to `low` in the API to cut latency.

## Basic agent (p16) + model routing (p18)

```ts
import { Memory } from '@mastra/memory'
import { Agent } from '@mastra/core/agent'

export const agent = new Agent({
  name: 'my-agent',
  instructions: 'You are a helpful assistant',
  model: 'openai/gpt-5.1',
})

const result = await agent.generate("What is the weather today?")
// one-line model/provider swap (model routing) — no SDK rip-out
```

## Structured output (p19)

```ts
import { z } from 'zod'
const response = await agent.generate('Help me plan my day.', {
  structuredOutput: {
    schema: z.array(z.object({ name: z.string(), activities: z.array(z.string()) })),
  },
})
```
Route structured-extraction to a cheaper/faster model — it needs less reasoning.

## Tool calling (p20-21)

```ts
import { createTool } from "@mastra/core/tools"
import { z } from "zod"

export const weatherTool = createTool({
  id: "Get Weather Information",
  description: "Fetches the current weather information for a given city",
  inputSchema:  z.object({ city: z.string().describe("City name") }),
  outputSchema: z.object({ temperature: z.number(), conditions: z.string() }),
  execute: async ({ context: { city } }) => { /* call weather API */ },
})
```
Best practices: detailed descriptions (what it does AND when to call it), specific I/O
schemas, semantic naming (`multiplyNumbers` not `doStuff`). "Designing your tools is the
most important step" — write the tool list before you code.

## Agent memory — three types + observational memory (p24-28)

Three types: **working memory** (durable user characteristics), **semantic recall**
(embed messages, RAG retrieve), **observational memory** (compress sessions into
structured observations).

Observational-memory observation log (formatted text, three-date model, emoji log levels):
```
Date: 2026-01-15
 - 🔴 12:10 User is building a Next.js app with Supabase auth, due in 1 week (Jan 22 2026)
 - 🔴 12:10 App uses server components with client-side hydration
 - 🟡 12:12 User asked about middleware configuration for protected routes
 - 🔴 12:15 User stated the app name is "Acme Dashboard"
```
Context window = two blocks: observations (~30k tokens reserved) + raw messages (~40k).
New messages append to block 2; when raw overflows, an **observer agent** compresses into
observations; when observations overflow, a **reflector agent** garbage-collects.

```ts
const agent = new Agent({
  name: 'my-agent',
  instructions: 'You are a helpful assistant',
  model: 'openai/gpt-5-codex',
  memory: new Memory({ options: { observationalMemory: true } }),
})
```

Memory processors (prune context before it hits the LLM):
```ts
import { Memory } from "@mastra/memory"
import { ToolCallFilter, TokenLimiter } from "@mastra/memory/processors"

const memory = new Memory({
  processors: [
    new ToolCallFilter(),                              // remove all tool calls
    new ToolCallFilter({ exclude: ["generateImageTool"] }), // or only noisy ones
    new TokenLimiter(127000),                          // ALWAYS place TokenLimiter last
  ],
})
```
Extend `MemoryProcessor` for custom logic. Prompt caching plays nicely with observational
memory (append-only prefix = cache hits).

## Dynamic agent (runtime config, p30)

```ts
const supportAgent = new Agent({
  name: "Dynamic Support Agent",
  instructions: async ({ runtimeContext }) => {
    const tier = runtimeContext.get("user-tier")
    const language = runtimeContext.get("language")
    // tailor support level + documentation by tier; respond in ${language}
  },
  model: ({ runtimeContext }) =>
    runtimeContext.get("user-tier") === "enterprise" ? "openai/gpt-4" : "openai/gpt-3.5-turbo",
  tools: ({ runtimeContext }) => {
    const baseTools = [knowledgeBase, ticketSystem]
    if (runtimeContext.get("user-tier") === "enterprise") baseTools.push(advancedAnalytics)
    return baseTools
  },
})
```

## Guardrails architecture (p32)

Input guardrails: prompt-injection guard, jailbreaking guard, privacy guard → input → LLM
→ output → Output guardrails: authorization guard, data-leakage guard, toxicity guard.
(Chris Bakke Dec-2023 injection: a dealership chatbot tricked into "$1, legally binding,
no takesies backsies.") For high-stakes/irreversible actions, add HITL checkpoints.

## MCP server + client (p40-41)

```ts
import { MCPServer } from "@mastra/mcp"
const server = new MCPServer({ name: "Weather Server", version: "1.0.0", tools: { weatherTool } })
await server.startStdio()

import { MCPClient } from "@mastra/mcp"
const mcp = new MCPClient({
  servers: {
    weather: { command: "npx", args: ["tsx", "weather-server.ts"] },   // stdio (local)
    stocks:  { url: new URL("http://localhost:1234/sse") },            // HTTP/SSE (remote)
  },
  timeout: 30000,
})
const agent = new Agent({ name: "Weather Agent", model: "openai/gpt-4", tools: await mcp.getTools() })
```
A proxy MCPServer can aggregate `await mcp.getTools()` from many servers.

## Workflows — branch/chain/merge/condition (p48-51)

`.step()` branches, `.then()` chains (each step waits, sees prior results), branches merge
at a `context` node, conditions are defined on the **child** step:
```ts
myWorkflow.step(
  new Step({ id: "processData", execute: async ({ context }) => { /* action */ } }),
  { when: { "fetchData.status": "success" } },
)
```
Best practices: meaningful I/O per step (so it shows in tracing); **decompose so the model
does one thing per step — no more than one model call in any step.**

## Suspend / resume (p53-55)

```ts
const myStep = createStep({
  id: "my-step",
  inputSchema:   z.object({ inputValue: z.string() }),
  outputSchema:  z.object({ outputValue: z.string() }),
  resumeSchema:  z.object({ resumeValue: z.string() }),   // optional
  suspendSchema: z.object({ suspendValue: z.string() }),  // optional
  execute: async ({ inputData, mastra, getStepResult, getInitData, runtimeContext }) => { /* ... */ },
})

const myWorkflow = createWorkflow({ id: "my-workflow", inputSchema, outputSchema, steps: [step1, step2, step3] })
  .then(step1).then(step2).then(step3).commit()

const run = myWorkflow.createRun()
const result = await run.start({ inputData: { startValue: "initial data" } })
if (result.status === "suspended") {
  await run.resume({ step: result.suspended[0], resumeData: { /* user input */ } })
}
```
**In production, persist workflow state to a durable store — a suspended workflow that
lives only in memory won't survive a server restart.**

## RAG pipeline (p67-68)

```ts
import { MDocument } from "@mastra/rag"
import { PgVector } from "@mastra/pg"
import { embedMany } from "ai"
import { openai } from "@ai-sdk/openai"

const doc = MDocument.fromText("Your text content...")
const chunks = await doc.chunk({ strategy: "recursive", size: 512, overlap: 50 })
const { embeddings } = await embedMany({ values: chunks.map(c => c.text), model: openai.embedding("text-embedding-3-small") })

const pgVector = new PgVector("insert query here")
await pgVector.createIndex({ indexName: "embeddings", dimension: 1536 })
await pgVector.upsert("embeddings", embeddings, chunks.map(c => ({ text: c.text })))

const results = await pgVector.query("embeddings", queryEmbedding, topK)
const completion = await openai("gpt-4o-mini").generate(
  `Based on this context: ${context}. If the context lacks sufficient information, please state this explicitly.`
)
```
Alternatives to RAG (reach for first): give the agent search tools; let it run code; feed
full context (Gemini 1M, beware "context rot"); extract entities/relationships. "Build an
agent first. Use RAG as a fallback."

## Multi-agent patterns (p76-77)

Pattern grid: Single Agent · Network · Supervisor · Supervisor-as-tools · Hierarchical ·
Custom. "A hierarchy is just a supervisor of supervisors. Start with the simplest version."
```ts
const publisherAgent = new Agent({
  name: "publisherAgent",
  instructions: "You are a publisher agent that coordinates content creation. First call the copywriter for initial content, then the editor for refinement.",
  model: { provider: "ANTHROPIC", name: "claude-3-5-sonnet-20241022" },
  tools: { copywriterTool, editorTool },   // subagents wrapped as tools
})
```

## Eval — LLM-as-judge (p92) + tracing/eval UIs (p87, p90)

```ts
import { Agent } from "@mastra/core/agent"
import { createFaithfulnessScorer } from "@mastra/evals/scorers/prebuilt"
const evaluatedAgent = new Agent({
  scorers: { relevancy: createFaithfulnessScorer({ model: "openai/gpt-5.1" }) },
})
```
Tracing UI shows: trace view (per-step duration), input/output JSON, call metadata
(status, latency, total operations + $ cost). Eval UI shows: score distribution, per-eval
input/output/expected/score/duration, overall score per PR (regression gate).
LLM-as-judge caveats: judges prefer longer answers; pick a judge from a different model
family than the agent.

## Voice (p116)

```ts
import { Agent } from "@mastra/core/agent"
import { OpenAIVoice } from "@mastra/voice-openai"
const agent = new Agent({
  name: 'Agent',
  instructions: 'You are a helpful assistant with voice capabilities.',
  model: openai('gpt-4o'),
  voice: new OpenAIVoice(),
})
const audioStream = fs.createReadStream('/path/to.mp3')
const text = await agent.listen(audioStream)   // follow with agent.speak() to reply
```
End-to-end speech-to-speech (`gpt-realtime`) is emerging but struggles with turn-taking
(voice activity detection) and is costly (audio info density ~1/1000 of text).
