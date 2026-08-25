"""Databricks backend for `pipeline_mcp` (Phase 2).

`run_transform` triggers a Lakeflow Declarative Pipeline update;
`get_quality_metrics` reads back `event_log(<pipeline_id>)` violation
metrics. Implementation lands in Phase 2; Phase 0 only fixes the shape of
the seam.
"""

from __future__ import annotations

from typing import Any

from mcp_servers.pipeline_mcp.backends.base import PipelineBackend


class DatabricksBackend(PipelineBackend):
    def __init__(self) -> None:
        raise NotImplementedError

    def run_transform(
        self, layer: str, full_refresh: bool, tables: list[str] | None
    ) -> dict[str, Any]:
        raise NotImplementedError

    def get_quality_metrics(self, run_id: str) -> dict[str, Any]:
        raise NotImplementedError
