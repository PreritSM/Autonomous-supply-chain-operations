"""Forecasting agent (Build Spec §6).

Reads ``fct_daily_demand`` via the warehouse MCP server, runs the LightGBM demand
model (see forecasting/), produces per-SKU forecasts, and flags statistical
anomalies with a simple z-score / IQR check (kept honest and cheap, not
over-engineered). Writes an audit entry with the forecast summary + anomaly count.
"""

from __future__ import annotations

# from agents.state import PipelineState


def forecasting_agent(state):  # -> PipelineState
    """TODO: implement per §6."""
    raise NotImplementedError
