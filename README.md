# Agentic Data Pipeline — Autonomous Supply Chain

> I built an agentic pipeline that autonomously detects and quarantines bad data,
> transforms it through versioned dbt models, forecasts demand, and explains its
> own decisions — **validated against injected data defects, not just clean-data
> accuracy.**

Four LangGraph-orchestrated agents turn messy, disruption-prone retail data (the
M5 competition dataset) into a validated demand forecast with a human-readable
audit trail. A self-written **disruption injector** corrupts a controlled,
*logged* fraction of the input data across five defect types, so the pipeline's
catch rate is a real precision/recall number scored against ground truth — not a
vibe. That is the single thing separating this from a generic forecasting demo.

Built to read credibly to two audiences at once: a **Data Engineer II** panel
(warehouse modeling, dbt, PySpark, lineage/audit) and an **Agentic-AI / MLOps**
panel (LangGraph, MCP, multi-agent orchestration, a real feedback loop).

## Architecture

Four agents, **LangGraph-orchestrated**, with **one real feedback loop**. The
graph itself is the orchestrator — it owns shared state and routes control; there
is no separate orchestrator agent.

| Agent | Role |
|---|---|
| **`ingestion_agent`** | Profiles incoming files via `landing_zone_mcp`, runs quality checks, quarantines bad rows into a `quarantine` table with a `QualityIssue` reason attached. |
| **`transformation_agent`** | Triggers `dbt run`/`dbt test` over the clean staged rows via `pipeline_mcp`; maps raw → conformed through staging → intermediate → marts. Records row counts in/out and dbt test failures. |
| **`forecasting_agent`** | Reads `fct_daily_demand` via `warehouse_mcp`, runs the LightGBM demand model, flags statistical anomalies (z-score / IQR). |
| **`validator_agent`** | Reconciles outputs (row-count continuity, forecast vs. naive baseline), writes the human-readable audit report, and **can set `discrepancy_flag=True` to route control back to the transformation agent.** |

```
                ┌─────────────┐
   new files →  │  ingestion  │──quarantine──▶ quarantine table
                └──────┬──────┘
                       │ clean rows
                       ▼
                ┌──────────────┐        ◀── discrepancy_flag=True
        ┌──────▶│transformation│               (max-retry capped)
        │       └──────┬───────┘
        │              │ conformed marts
        │              ▼
        │       ┌─────────────┐
        │       │ forecasting │
        │       └──────┬──────┘
        │              │ forecast + anomalies
        │              ▼
        │       ┌─────────────┐
        └───────│  validator  │──▶ audit report (bi_agent_audit_log)
                 └─────────────┘
```

The feedback loop (validator → transformation) is the centerpiece of the
"agentic" claim — without it this is a linear script with LLM commentary. At
least one scenario (a corrupted calendar join) is deliberately engineered to
trigger it, and the graph edge is guarded with a max-retry cap.

Agents reach tools **only** through three custom MCP servers — this is also the
backend abstraction seam (`WAREHOUSE_BACKEND=postgres|databricks`); no agent
contains backend-conditional code.

| MCP server | Tools |
|---|---|
| `warehouse_mcp` | `query(sql)` (read-only) · `write_table(table, rows)` · `get_row_count(table)` |
| `landing_zone_mcp` | `list_new_files()` · `read_file(path)` · `move_to_quarantine(path, reason)` |
| `pipeline_mcp` | `run_transform(layer, full_refresh, tables)` · `get_quality_metrics(run_id)` |

Shared state is a single `PipelineState` TypedDict (`agents/state.py`) threaded
through the whole graph — `run_id`, `quarantined_rows`, `conformed_table`,
`forecast`, `anomalies`, `discrepancy_flag`, `audit_log`, `status`. Every agent
appends a plain-English line to `audit_log` before returning; that log is what
the validator turns into the final narrative report.

## The disruption injector — why the eval numbers are trustworthy

`disruption_injector/inject.py` corrupts a controlled fraction of clean M5 data
and logs exactly which rows/cells it touched, across five defect types:

- `missing_values`
- `duplicate_rows`
- `schema_drift`
- `out_of_range`
- `type_corruption`

`inject(df, disruption_type, rate, seed)` returns `(corrupted_df,
ground_truth_issues)`. The ingestion agent's quality rules map 1:1 onto these
five categories, so **catch rate = `detected ∩ actual / actual`** is a real,
reproducible metric — not a claim.

## Data model (dbt)

Four layers, deliberately not more:

```
staging          intermediate              marts                    bi
─────────        ──────────────            ─────────────            ────────────────────
stg_sales    ┐                                                      bi_forecast_vs_actual
stg_calendar ├──▶ int_sales_enriched  ──▶  fct_daily_demand  ──▶     bi_data_quality_summary
stg_prices   ┘    (sales+calendar+price)   (forecasting agent      bi_agent_audit_log
                                             reads this)             bi_anomaly_overlay
```

`bi` is materialized as tables (import-mode performance) and is the only layer
Power BI ever points at.

## Backends

Postgres is the **default backend and the demo path** — clone, `docker-compose
up`, three commands, done. Databricks (Lakeflow Declarative Pipelines) is a
**second backend behind the same MCP seam**, not a replacement:

| | Postgres (default) | Databricks (stretch) |
|---|---|---|
| Bronze → silver | dbt staging layer | DLT (Auto Loader over a Unity Catalog Volume) |
| Silver → gold → bi | dbt | dbt-databricks (identical SQL to Postgres from `int_sales_enriched` down) |
| Quality enforcement | ingestion agent + quarantine table | ingestion agent emits rules to `pipeline_config.expectations`; DLT flags via `is_quarantined` + `failed_rules` (never `expect_or_drop` — would destroy the row IDs the eval harness joins against) |
| Agents run | locally | locally (control/data plane split; Free Edition serverless has restricted outbound internet) |

The full disruption-rate eval matrix always runs on Postgres — Databricks Free
Edition has a daily quota shutdown; Databricks is run once per rate for demo
screenshots.

## Run it yourself

```bash
docker-compose up -d               # Postgres warehouse (port 5432 on host)
uv sync                            # install deps

uv run disruption_injector/inject.py --rate 0.15 --seed 42   # corrupt a slice of data, log ground truth
uv run agents/graph.py --run-id <id>                          # run the four-agent LangGraph pipeline

cd dbt && dbt run && dbt test      # rebuild + test the staging→intermediate→marts→bi layers
uv run eval/harness.py             # full 0/5/15/30% disruption-rate matrix + metrics
```

Each `eval/harness.py` run reports:

- **defect catch rate** and **false-quarantine rate** (headline, vs. injector ground truth)
- dbt test pass rate
- forecast accuracy (WRMSSE / MAPE on held-out M5 weeks)
- anomaly precision (vs. synthetically injected demand shocks)
- end-to-end latency

## Power BI reporting (additive polish)

Four pages, all built on the `bi` schema through a read-only `powerbi_reader`
user, Import mode:

1. **Forecast vs. Actual** — hierarchy drill-down state → store → category → item
2. **Data Quality Health** — catch rate by disruption type × rate (the headline claim, made visual)
3. **Agent Audit Trail** — the agents' plain-English reasoning, feedback-loop rows highlighted
4. **Anomaly Overlay** — injected vs. model-detected demand shocks

## Repo layout

```
agents/               graph.py (StateGraph), state.py (PipelineState),
                       {ingestion,transformation,forecasting,validator}_agent.py
mcp_servers/
  warehouse_mcp/       server.py + backends/{base,postgres,databricks}.py
  landing_zone_mcp/    server.py + backends/{base,local_fs,uc_volume}.py
  pipeline_mcp/        server.py + backends/{base,dbt,databricks}.py
databricks/            (Phase 2) pipelines/bronze_silver.py, pipeline.json, setup.sql
dbt/                   dbt_project.yml, profiles.yml, models/{staging,intermediate,marts,bi}/
disruption_injector/   inject.py — corrupts clean data on purpose, logs ground truth
forecasting/           train.py, model.py — LightGBM / Prophet baseline
eval/                  harness.py, metrics.py
data/                  raw/ (M5 source lands here), landing/ (disruption-injected files)
docker-compose.yml     Postgres warehouse (+ optional Spark)
notebooks/             exploration.ipynb
```

## Dataset

Standard [M5 competition](https://www.kaggle.com/competitions/m5-forecasting-accuracy)
files, keyed by `item_id` × `store_id` (10 stores across CA/TX/WI, 30,490
series): daily sales (`sales_train_*`), a `calendar.csv` with events and SNAP
eligibility, weekly `sell_prices.csv`, and WRMSSE hierarchy weights. Most series
are intermittent (long zero-sales stretches), which is why the forecasting agent
needs more than a moving average and why price/event/SNAP features actually flow
through the transformation layer instead of being dropped.

## Scope discipline

Not a production supply-chain platform. Public/synthetic data only. The
dashboard is additive polish, not a priority over the CLI/README demo path. Not
chasing SOTA forecast accuracy — the agentic data-quality loop is the lead, the
forecasting model is a supporting character.

## Results

_(populated by `eval/harness.py` — defect catch rate, false-quarantine rate, and
forecast accuracy at each disruption level. The catch-rate-vs-disruption chart
is the key portfolio visual: it demonstrates self-healing under increasing
disruption rather than asserting it.)_

<!-- ## Status

Scaffold only — structure created against the Build Spec, agents/servers/models
are stubs pending implementation. See `Agentic_Data_Pipeline_Build_Spec.md` for
the detailed spec and `Claude_Code_Handoff_Document.md` for the business framing
and decisions. -->
