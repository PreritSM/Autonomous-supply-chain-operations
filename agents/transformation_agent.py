"""Transformation agent (Build Spec §6).

Triggers ``dbt run`` (subprocess tool call) over the clean staged rows, mapping
raw → conformed through the dbt layers:

    staging (stg_sales, stg_calendar, stg_prices)
      → intermediate (int_sales_enriched: joins sales + calendar + prices)
        → marts (fct_daily_demand — what the forecasting agent reads)

Records row counts in/out and any dbt test failures in the audit log. Re-entered
by the validator's feedback loop when ``discrepancy_flag`` is set.
"""

from __future__ import annotations

# from agents.state import PipelineState


def transformation_agent(state):  # -> PipelineState
    """TODO: implement per §6."""
    raise NotImplementedError
