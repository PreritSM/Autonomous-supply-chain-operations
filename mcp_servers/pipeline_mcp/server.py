"""pipeline_mcp — MCP server wrapping the transform/orchestration trigger
(Build Spec §7 amendment, ratified 2026-08-25, see Claude_Plan/DECISIONS.md).

Exists so `transformation_agent.py` never contains backend-conditional code
(`if backend == "databricks"`). Backend is selected at startup via
`PIPELINE_BACKEND=dbt|databricks` — these tool signatures never change, only
the backend implementation swaps. On the Postgres backend, `run_transform`
shells out to `dbt run`/`dbt test`; on the Databricks backend it triggers the
DLT pipeline update and `get_quality_metrics` reads back the pipeline event
log. Keep it clean (~100–150 lines with the official Python MCP SDK).

Tools exposed:
    run_transform(layer: str, full_refresh: bool, tables: list[str] | None)
        -> triggers the transform for the given backend, returns run status
    get_quality_metrics(run_id: str)
        -> dbt test results (Postgres) or event-log violation metrics (Databricks)
"""

from __future__ import annotations

import os
from typing import Any

from mcp.server.mcpserver import MCPServer

from mcp_servers.pipeline_mcp.backends.base import PipelineBackend

mcp = MCPServer("pipeline_mcp")


def _load_backend() -> PipelineBackend:
    name = os.environ.get("PIPELINE_BACKEND", "dbt")
    if name == "dbt":
        from mcp_servers.pipeline_mcp.backends.dbt import DbtBackend

        return DbtBackend()
    if name == "databricks":
        from mcp_servers.pipeline_mcp.backends.databricks import DatabricksBackend

        return DatabricksBackend()
    raise ValueError(f"Unknown PIPELINE_BACKEND: {name!r} (expected dbt|databricks)")


_backend: PipelineBackend | None = None


def _get_backend() -> PipelineBackend:
    # Lazy so importing this module doesn't require a live backend — the
    # stub backends raise NotImplementedError from __init__ until Phase 1/2.
    global _backend
    if _backend is None:
        _backend = _load_backend()
    return _backend


@mcp.tool()
def run_transform(
    layer: str, full_refresh: bool = False, tables: list[str] | None = None
) -> dict[str, Any]:
    """Trigger the transform for the active backend; returns run status."""
    return _get_backend().run_transform(layer, full_refresh, tables)


@mcp.tool()
def get_quality_metrics(run_id: str) -> dict[str, Any]:
    """dbt test results (Postgres) or event-log violation metrics (Databricks)."""
    return _get_backend().get_quality_metrics(run_id)


def main() -> None:
    """Run the pipeline MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
