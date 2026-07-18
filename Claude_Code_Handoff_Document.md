# Project Handoff: Agentic Data Pipeline (Autonomous Supply Chain)

**This document is context, not a spec.** Detailed planning (repo structure, task breakdown, sprint order) happens in the Claude Code session itself. What follows is the *why* behind the project, the decisions already made and the reasoning behind them, and what "done" needs to look like — so the build stays anchored to its actual purpose instead of drifting into a generic ML demo.

---

## 1. Who's building this and why

I'm Prerit Mittal, an M.S. Computer Engineering candidate (RIT, graduating May 2026), ~1.5 years of SWE experience at GE Digital, currently job-hunting for junior AI/ML Engineer, MLOps Engineer, and Agentic AI/RAG roles. This project is a flagship portfolio piece, not a class assignment or a toy — it needs to survive scrutiny from a technical interviewer.

The immediate trigger: I went through a QuantumBlack (McKinsey) Data Engineer II phone screen and was rejected. In prepping for and reflecting on that loop, I identified specific gaps in my profile — no production PySpark experience, no hands-on dbt, thin exposure to warehouse-style data modeling (Snowflake/BigQuery-equivalent patterns). This project is deliberately designed to close those gaps *while* staying true to my actual strength and interest: agentic AI, multi-agent orchestration, and MLOps (LangGraph, RAG, MCP, MLflow, DVC — my existing stack from the Adaptive Multi-Agent RAG System and the Wafer Quality MLOps pipeline).

So this project has two audiences at once: it needs to read as a serious data-engineering deliverable to a Data Engineer II panel, *and* as a serious agentic-AI system to an AI/ML Engineer or Agentic AI panel. Every design decision below was made with both audiences in mind.

---

## 2. Where the idea came from

I worked through Deloitte AI Institute's 2026 *AI Dossier* (278 pages, 130 use cases across six industries, 81 tagged "Agentic AI") specifically to find a use case that would make a strong flagship project. I filtered against four criteria:

1. **High agentic complexity** — genuine multi-agent roles, not one LLM call wearing different hats
2. **Advanced tooling integration** — a natural fit for MCP and tool calling, not bolted on
3. **Low data barrier** — public dataset/API only, no proprietary or credentialed data
4. **Maximum resume impact** — addresses a real, high-value business bottleneck

That process produced a shortlist of 10 candidates. I initially ranked an "AI agents for software engineering" use case near the top, but rejected it after realizing: (a) autonomous coding agents are the most saturated category in the entire space right now — every job-hunter has some version of this, so it doesn't differentiate; (b) it's brutally hard to benchmark fairly, because any public score gets compared against frontier-lab systems (Claude/Devin-class) with far more engineering behind them, making a solo build look weak by comparison rather than impressive; and (c) "fix an arbitrary bug in an arbitrary repo" is open-ended enough that a lot of build time goes into fighting garbage outputs instead of demonstrating architecture.

**This project — the agentic data pipeline — was selected instead** because it has a fixed, bounded task (ingest → validate → transform → forecast → explain), an objective metric that doesn't compete against a public leaderboard of frontier labs, and it happens to map directly onto the exact gaps from the QuantumBlack loop.

The dossier's actual use case is "Autonomous supply chain operations" (Consumer industry section, tagged Agentic AI). Deloitte's framing names a data-readiness agent (quality checks, exception detection), a data-generator agent (raw → structured), an optimization agent, a demand-mapping agent, and a validation/explanation agent. I stripped the supply-chain-specific language and kept the underlying shape: an autonomous pipeline that ingests messy data, catches its own defects, transforms it properly, forecasts on it, and explains its own reasoning.

---

## 3. The business problem this is actually modeling

The pain point isn't "we need a forecast" — it's the **bullwhip effect**: small, noisy demand signals get amplified into large, costly swings as they move up a supply chain, and a major cause is forecasting run on delayed, siloed, or quietly-bad data rather than the demand signal itself. A pipeline that can't tell good data from bad data, or can't explain why it produced a given forecast, makes the bullwhip problem worse, not better — because decisions get made on numbers nobody can audit.

That's the narrative this project needs to *prove*, not just describe: that an agentic system can catch data problems before they propagate into a bad forecast, and that it can explain itself well enough that a human would actually trust the number.

---

## 4. What "done" looks like — the core claim to prove

> "I built an agentic pipeline that autonomously detects and quarantines bad data, transforms it through versioned dbt models, forecasts demand, and explains its own decisions — validated against injected data defects, not just clean-data accuracy."

The key design decision that makes this provable rather than just plausible: **I write my own disruption injector.** Instead of trusting the pipeline to "just work" on clean Kaggle data, I deliberately corrupt a controlled, logged fraction of the input (missing values, duplicates, schema drift, out-of-range values, type corruption) and score the pipeline's actual catch rate against that ground truth. This turns "self-healing" from a claim into a measured precision/recall number. This is non-negotiable — it's the single thing that separates this from a generic forecasting demo.

---

## 5. Architecture decisions already made

**Four agents, LangGraph-orchestrated, with one real feedback loop:**

1. **Ingestion/Readiness agent** — profiles incoming data, runs quality checks, quarantines bad rows with reasons attached
2. **Transformation agent** — maps raw → conformed schema via dbt models (staging → intermediate → marts)
3. **Forecasting agent** — runs the demand model, flags statistical anomalies
4. **Validator/Explainer agent** — reconciles outputs, writes a human-readable audit rationale, and — this is the important part — can flag a discrepancy that routes control **back** to the transformation agent for re-processing

That feedback loop matters. Without it, this is a linear script with LLM commentary attached. With it, there's a real instance of one agent's output changing another agent's control flow — genuine multi-agent behavior, not agent-flavored scripting. Whatever gets planned in Claude Code needs to preserve this loop as a real, demoable path (i.e., deliberately construct at least one scenario that triggers it — don't leave it to chance).

**Why LangGraph:** I already know this framework from a prior project (Adaptive Multi-Agent RAG System — Router/Retriever/Fact-Checker/Synthesizer/Generator nodes), so the orchestration patterns, state-passing conventions, and self-reflection/uncertainty-gating logic from that project transfer directly. Reuse that muscle memory rather than re-deriving agent patterns from scratch.

**Why MCP is required, not optional:** Tool access needs to go through custom or standard MCP servers (a warehouse MCP wrapping Postgres/DuckDB, a landing-zone MCP wrapping the raw-file directory), not inline API calls. Authoring a real MCP server is itself a portfolio artifact — "I called an API" is a materially weaker line than "I authored an MCP server exposing X to agents." Keep this code clean; it's not scaffolding, it's a thing to point at.

---

## 6. Dataset decision and why

**M5 Forecasting — Accuracy (Kaggle)** — Walmart hierarchical sales data, 10 stores, 3 categories, ~3,049 products, with calendar and pricing tables. Public, free, no credentialing.

Chosen over alternatives (e.g., Olist) for two specific reasons:
- **Hierarchical structure** (item → department → category → store → state) gives the dbt marts a genuine reason to exist — there's real aggregation logic to model, not just a flat pass-through.
- **A known, citable public benchmark metric** (WRMSSE) — this means the forecasting number in the eval report is something a reviewer can contextualize against, rather than an accuracy figure with no reference point.

Two properties of this dataset drive design requirements downstream: the majority of the 42,840 time series display **intermittency** (long stretches of zero sales), which is exactly what breaks naive forecasting approaches and is why the forecasting agent needs more care than a moving average; and the data includes real exogenous variables (price, promotions, calendar events) that need to actually flow through the transformation layer, not just get dropped.

---

## 7. Tech stack decisions and the reasoning behind each

| Choice | Reasoning |
|---|---|
| **Postgres (or DuckDB)** as warehouse | Real warehouse behavior for the QuantumBlack narrative; Postgres reads better on a resume, DuckDB is faster to iterate with locally — open decision, pick based on how much local infra pain is acceptable |
| **dbt-core** for transformation | Directly closes the named gap from the QuantumBlack loop. The model itself (M5) doesn't strictly need 3 dbt layers — they're included for the skill signal, so don't let this sprawl into unnecessary complexity beyond what's needed to look real (staging → intermediate → marts is enough) |
| **PySpark** for the heavy transform step (optional stretch) | Also a named gap; only worth the extra time if there's room in the schedule — the core claim doesn't depend on it |
| **Great Expectations or a lightweight custom rule engine** for data quality | The readiness agent needs real validation logic to call, not hand-waved checks — favor whichever is faster to get genuinely working over whichever sounds more impressive |
| **LightGBM (or Prophet)** for the forecasting model | The model is deliberately not the point of this project — the agentic data-quality loop is. Don't let model tuning eat the schedule; a solid baseline is enough |
| **Claude (Sonnet) via API** for agent reasoning | Consistent with prior projects |

---

## 8. Evaluation philosophy

Every agent should be scored against something objective, not vibes:

- **Defect catch rate / false quarantine rate** — measured against the disruption injector's ground-truth log (this is the headline metric)
- **dbt test pass rate** — native dbt tests (not_null, unique, relationships)
- **Forecast accuracy (WRMSSE or MAPE)** — against held-out M5 weeks, a number a reviewer can recognize
- **Anomaly precision** — against synthetically injected demand shocks

Running the eval across a matrix of disruption rates (e.g., 0%, 5%, 15%, 30% corrupted) and showing how catch rate and forecast accuracy hold up under increasing disruption is a strong, honest way to demonstrate the "self-healing" claim rather than assert it.

---

## 9. What I'm expecting out of the Claude Code build session

- A working repo, not a notebook — this needs to run end to end via a small number of commands (e.g., `docker-compose up`, one command to inject disruptions, one to run the graph)
- The feedback loop (validator → transformation) needs to actually fire at least once in the demo path, deliberately engineered, not hoped-for
- A results artifact (table or chart) showing the eval metrics across the disruption-rate matrix — this is the thing that gets screenshotted into the README and talked about in interviews
- A README that leads with the one-line pitch (Section 4 above), shows the architecture, and includes a sample of the validator agent's actual plain-English audit output — that output is the single artifact that visibly proves this is agentic, not just a pipeline with an LLM summary bolted on at the end
- Scope discipline: this is not a production supply-chain platform. If a design choice doesn't serve either (a) the agentic-AI narrative or (b) the data-engineering narrative, it's probably out of scope

---

## 10. Constraints and non-goals

- No proprietary or credentialed data, anywhere in the pipeline — public/synthetic only (this was a hard filter from the start, not a compromise)
- Not building a UI/dashboard as a priority — a clean CLI/README demo path matters more than a polished frontend
- Not chasing state-of-the-art forecasting accuracy — the model is a supporting character, the agentic data-quality loop is the lead
- Timeline: originally scoped at ~7–10 days core build, +2 days if PySpark/deeper dbt work gets included — treat this as a guide, not a hard deadline, but a useful signal for how much to gold-plate any one piece
