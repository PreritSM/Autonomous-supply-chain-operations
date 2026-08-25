# Agentic Data Pipeline — Autonomous Supply Chain

> I built an agentic pipeline that autonomously detects and quarantines bad data,
> transforms it through versioned dbt models, forecasts demand, and explains its
> own decisions — **validated against injected data defects, not just clean-data
> accuracy.**

Four LangGraph-orchestrated agents turn messy, disruption-prone retail data (M5)
into a validated demand forecast with a human-readable audit trail. A self-written
disruption injector corrupts a controlled, *logged* fraction of the input, so the
pipeline's catch rate is a real precision/recall number scored against ground
truth — not a vibe. That is the single thing separating this from a generic
forecasting demo.

## Architecture

Four agents, one real feedback loop (validator → transformation). The LangGraph
graph itself is the orchestrator — it owns shared state and routes control.

| Agent | Role |
|---|---|
| **Ingestion / readiness** | Profiles incoming files (landing-zone MCP), runs quality checks, quarantines bad rows with a `QualityIssue` reason. |
| **Transformation** | Triggers `dbt run` over clean rows: staging → intermediate → marts. Records row counts + dbt test failures. |
| **Forecasting** | Reads `fct_daily_demand` (warehouse MCP), runs the LightGBM demand model, flags anomalies (z-score / IQR). |
| **Validator / explainer** | Reconciles outputs, writes the audit report, can set `discrepancy_flag=True` to route control back to transformation. |

Agents reach tools **only** through three custom MCP servers (`warehouse_mcp`,
`landing_zone_mcp`, `pipeline_mcp`).

## Run it yourself

```bash
docker-compose up -d          # Postgres warehouse (port 5432 bound to host)
uv sync                       # install deps
# TODO: load raw M5 → raw schema
# TODO: inject disruptions   (disruption_injector/inject.py)
# TODO: run the graph        (agents/graph.py)
# TODO: dbt run && dbt test  (dbt/)
# TODO: eval harness across the 0/5/15/30% disruption matrix (eval/)
```

## Status

Scaffold only — structure created against the Build Spec, agents/servers/models
are stubs pending implementation. See `Agentic_Data_Pipeline_Build_Spec.md` for
the detailed spec and build plan.

## Results

_(populated by the eval harness — defect catch rate, forecast WRMSSE, and
false-quarantine rate at each disruption level.)_
