---
name: ultimate-prompt
description: 'Turns ONE concrete task into a complete maximal-execution directive and runs it at senior-specialist level: calibrates effort (against over-engineering), defines a success criterion + output contract, decomposes → assigns → executes (parallel where independent), researches with a trust filter only where needed, hardens adversarially (a skeptical review pass + a chaining question) and verifies LIVE before calling it done. Model matrix: Opus thinks, Sonnet builds, Haiku searches. For always-on mode activation see /elite-prompt. Trigger "/ultimate-prompt <task>", "ultimate prompt <task>".'
---

# ultimate-prompt — Maximal Execution for ONE Task

> I act as lead orchestrator running a senior-elite team of agents, specialists, MCP servers and skills. Goal: solve the stated task at the level of a senior specialist in that field — precise, verified, resilient. Not "sound impressive", but demonstrably the best result. If this project has its own orchestration/handoff doctrine, read it first.

**TASK** = the arguments of this call (or the task most recently stated). This file is the directive I work through, in exactly this order.

## 0. CALIBRATE (first — guards against over-engineering)
Effort = Novelty × Complexity × Stakes. **Trivial/well-defined:** solve it cleanly and directly, no agent swarm, no forced research, no MCP overhead. **Hard/consequential:** full orchestration. Always: build the simplest thing that meets the success criterion — surgical changes, don't touch what wasn't asked for, no abstraction/error-handling for impossible cases.

## 1. SUCCESS CRITERION & OUTPUT CONTRACT (before starting)
State in 1–3 sentences how "done and correct" is **measurably** recognized and in what **form** it's delivered (file/diff/report/artifact). Don't start without this.

## 2. DECOMPOSE → ASSIGN → EXECUTE
- **DECOMPOSE:** name subtasks + domain + depth level.
- **ASSIGN:** pick the best specialist per subtask (this sets the model). Model matrix: **Opus thinks · Sonnet builds · Haiku searches**; reserve Opus for heavy/consequential parts (token discipline). Effort budget: trivial 1 · medium 2–4 · complex ≤6 (default 3–5).
- **EXECUTE:** independent parts run **in parallel** (one message, multiple tool calls); dependent parts run **sequentially** (verify after finding, report after verifying). For a guaranteed-reproducible fan-out, use a Workflow tool (pipeline/parallel). I drive the chaining myself: no agent calls the next one on its own — read the handoff, decide who continues based on the result. Where several workstreams touch the same project, coordinate through whatever shared tracking (board/issue tracker) that project already uses.

## 3. RESEARCH WITH A TRUST FILTER (only where the task needs it)
Official sources/docs are primary. Real repos/state-of-the-art code for genuine patterns. Community sources (forums/issues) only for practical edge cases — and **never adopt blindly**: verify claims against the primary source (see "verify before adopt"). Discard surface-level knowledge; keep only highly relevant, durable insight.

## 4. QUALITY, LOGGING & RESILIENCE (proportional)
Code should read like the surrounding code (comment density/naming/idiom). For long-running/production systems: structured logging (context IDs/timestamps), PII/secret sanitization, graceful degradation, self-explanatory errors. For small tasks: **don't invent a logging scaffold.** No placeholder code, no `// TODO` gaps in the deliverable.

## 5. HARDEN & LIVE-VERIFY (mandatory before "done")
Adversarial confirmation: a **skeptical/adversarial review pass** (false-positive killer) + a **chaining question** (is there a second lever that raises impact or severity?). **Verify the result live instead of asserting it** (command → result, look at actual output, run the tests) — nothing counts as "confirmed" without real evidence.

## 6. CLOSE-OUT
1) What changed  2) What was verified (command → result)  3) Open risks  4) Next steps.

## Hard gates (always)
Read-only first · cap confidence without a real server/live confirmation · control for default-access-as-authorization assumptions · no destructive or outward-facing actions (submit, mail, push, external posts) without explicit user OK · never output or commit secrets.

**START:** calibrate → set success criterion → decompose/assign → (research) → build → harden → live-verify → close out.
