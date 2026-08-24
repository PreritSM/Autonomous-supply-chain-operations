"""LangGraph StateGraph wiring for the pipeline.

The graph is the orchestrator (Build Spec §2): it owns ``PipelineState`` and
routes control across the four agent nodes. The one real feedback loop —
validator → transformation, triggered when ``discrepancy_flag`` is set — is the
centerpiece of the "agentic" claim, so it must be a genuine, demoable edge.

Guard that edge with a max-retry cap so a persistent discrepancy can't loop
forever.

    ingestion → transformation → forecasting → validator ─┬─▶ done
                     ▲                                     │
                     └──────── discrepancy_flag ───────────┘
                              (capped by MAX_REPROCESS)
"""

from __future__ import annotations

# from langgraph.graph import END, StateGraph
# from agents.state import PipelineState
# from agents.ingestion_agent import ingestion_agent
# from agents.transformation_agent import transformation_agent
# from agents.forecasting_agent import forecasting_agent
# from agents.validator_agent import validator_agent

MAX_REPROCESS = 2  # feedback-loop retry cap; see Build Spec §13


def build_graph():
    """Construct and compile the pipeline StateGraph. TODO: implement (§2, §6)."""
    raise NotImplementedError
