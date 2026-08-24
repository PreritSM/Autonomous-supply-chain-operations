"""Validator / explainer agent (Build Spec §6).

Reconciles outputs: does the row count entering forecasting match what ingestion
approved (via warehouse MCP ``get_row_count``)? Do forecasts look sane against a
naive baseline (last-year-same-week)?

If something is off, sets ``discrepancy_flag = True`` with a reason — this routes
control back to the transformation agent in the graph, the genuine multi-agent
feedback loop. On success, writes the final human-readable report: data-quality
summary, transformation lineage, forecast + confidence, anomaly list, and a
plain-English rationale.
"""

from __future__ import annotations

# from agents.state import PipelineState


def validator_agent(state):  # -> PipelineState
    """TODO: implement per §6. Owns the discrepancy_flag feedback edge."""
    raise NotImplementedError
