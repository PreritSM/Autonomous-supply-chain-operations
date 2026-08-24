"""Ingestion / readiness agent (Build Spec §6).

Reads a new file via the landing-zone MCP server, runs quality checks (missing
values, out-of-range quantities/prices, schema drift, duplicate rows), and
quarantines failing rows into a ``quarantine`` table (warehouse MCP), tagging
each with a ``QualityIssue``. Passes clean rows forward and appends a one-line
audit summary, e.g. "Quarantined 214 of 12,050 rows: 180 missing unit_price,
34 duplicate order_id".

The quality rules must line up 1:1 with the injector's ground-truth categories
so the eval catch-rate is a real precision/recall number.
"""

from __future__ import annotations

# from agents.state import PipelineState, QualityIssue


def ingestion_agent(state):  # -> PipelineState
    """TODO: implement per §6. Reaches tools only through the MCP servers."""
    raise NotImplementedError
