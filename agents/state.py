"""Shared LangGraph state for the agentic supply-chain pipeline.

See Build Spec §5. The graph itself is the orchestrator: it owns this state and
routes control between the four agent nodes based on each agent's output.

Every agent MUST append a plain-English line to ``audit_log`` before returning.
That trail is what makes the validator's final report a narrative rather than a
JSON dump — and it's the artifact screenshotted for the README.
"""

from __future__ import annotations

from typing import Literal, TypedDict

from pydantic import BaseModel

# Issue categories line up 1:1 with the disruption injector's ground-truth types
# (disruption_injector/inject.py). Keep them in sync — the eval catch-rate metric
# joins on these.
IssueType = Literal["missing", "out_of_range", "schema_drift", "duplicate", "type_mismatch"]

Status = Literal[
    "ingesting",
    "transforming",
    "forecasting",
    "validating",
    "reprocessing",
    "done",
]


class QualityIssue(BaseModel):
    """One flagged defect, emitted by the ingestion/readiness agent."""

    row_id: str
    column: str
    issue_type: IssueType
    detail: str


class PipelineState(TypedDict):
    run_id: str
    raw_file_path: str
    quarantined_rows: list[QualityIssue]
    clean_row_count: int
    conformed_table: str | None          # dbt output table name
    forecast: dict | None                # {date, sku, predicted_demand, confidence}
    anomalies: list[dict]
    discrepancy_flag: bool               # set by validator to trigger the feedback loop
    discrepancy_reason: str | None
    audit_log: list[str]                 # human-readable trail, appended by every agent
    status: Status
