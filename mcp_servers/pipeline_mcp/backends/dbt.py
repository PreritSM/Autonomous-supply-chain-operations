"""dbt/Postgres backend for `pipeline_mcp` — the default backend (Phase 1).

`run_transform` shells out to `dbt run`/`dbt test`; `get_quality_metrics`
reads back the dbt test results for a run. Implementation lands in Phase 1;
Phase 0 only fixes the shape of the seam.
"""

from __future__ import annotations

from typing import Any

from mcp_servers.pipeline_mcp.backends.base import PipelineBackend


class DbtBackend(PipelineBackend):
    def __init__(self) -> None:
        raise NotImplementedError

    def run_transform(
        self, layer: str, full_refresh: bool, tables: list[str] | None
    ) -> dict[str, Any]:
        raise NotImplementedError

    def get_quality_metrics(self, run_id: str) -> dict[str, Any]:
        raise NotImplementedError
