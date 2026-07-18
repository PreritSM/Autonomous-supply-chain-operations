# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository state

This repository currently contains only the raw **M5 Forecasting Accuracy** competition dataset under `Dataset/` — there is no code, build system, or tests yet. No forecasting pipeline, notebooks, or scripts exist. When asked to build one, you'll be creating the project structure from scratch; check with the user on preferred language/tooling (Python is the de facto standard for M5 solutions) before scaffolding.

## Dataset (`Dataset/`)

Standard M5 competition files, keyed by `item_id` (product) x `store_id` (10 stores across CA/TX/WI):

- **`sales_train_validation.csv`** / **`sales_train_evaluation.csv`** — one row per item/store (30,490 series), columns `item_id, dept_id, cat_id, store_id, state_id` followed by daily unit sales columns `d_1` … `d_1913` (validation) / `d_1941` (evaluation, includes the validation period plus 28 more days).
- **`sales_test_validation.csv`** (`d_1914`–`d_1941`) / **`sales_test_evaluation.csv`** (`d_1942`–`d_1969`) — the 28-day holdout actuals for each phase, same row keys as the train files.
- **`calendar.csv`** — one row per date (`d_1` … `d_1969`), maps `d_n` day identifiers to calendar dates, weekday, month/year, event names/types (`event_name_1/2`, `event_type_1/2`), and SNAP (food-assistance) eligibility flags per state (`snap_CA`, `snap_TX`, `snap_WI`).
- **`sell_prices.csv`** — weekly (`wm_yr_wk`) sell price per `store_id` x `item_id`; large file (~6.8M rows). Join key to sales data is `store_id` + `item_id`, and to calendar via `wm_yr_wk`.
- **`weights_validation.csv`** / **`weights_evaluation.csv`** — WRMSSE aggregation weights per series at each hierarchy level (`Level_id` = Level1…Level12, from total to item/store), with `Dollar_Sales` and normalized `weight` columns.

Key relationships:
- `sales_*` rows join to `calendar.csv` by pivoting `d_n` columns against `calendar.date`.
- `sales_*` rows join to `sell_prices.csv` via `(store_id, item_id)`, then to `calendar.csv` via `wm_yr_wk` to get the price active on a given date.
- The competition metric (WRMSSE) requires aggregating series up the hierarchy (item/store → item → dept/store → dept → cat/store → cat → store → state → total) and weighting by `weights_*.csv`.
- "Validation" and "evaluation" are two phases of the same competition timeline: evaluation files are a strict superset — day ranges continue directly from where validation leaves off (`d_1914`→`d_1941` validation test period, `d_1942`→`d_1969` evaluation test period).
