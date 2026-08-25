"""pipeline_mcp — MCP server wrapping the transform/orchestration trigger (Build Spec §7 amendment,
ratified 2026-08-25, see Claude_Plan/DECISIONS.md).

Exists so `transformation_agent.py` never contains backend-conditional code
(`if backend == "databricks"`). On the Postgres backend, `run_transform` shells
out to `dbt run`/`dbt test`; on the Databricks backend it triggers the DLT
pipeline update and `get_quality_metrics` reads back the pipeline event log.
Keep it clean (~100–150 lines with the official Python MCP SDK).

Tools exposed:
    run_transform(layer: str, full_refresh: bool, tables: list[str] | None)
        -> triggers the transform for the given backend, returns run status
    get_quality_metrics(run_id: str)
        -> dbt test results (Postgres) or event-log violation metrics (Databricks)
"""

from __future__ import annotations

# from mcp.server.fastmcp import FastMCP
# mcp = FastMCP("pipeline_mcp")


def main() -> None:
    """Run the pipeline MCP server over stdio. TODO: implement per §7 amendment."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
