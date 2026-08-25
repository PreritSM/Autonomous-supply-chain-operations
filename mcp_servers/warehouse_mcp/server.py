"""warehouse_mcp — MCP server wrapping the warehouse (Build Spec §7, backend
seam per CLAUDE.md's "MCP is the backend abstraction" decision).

Agents reach the warehouse ONLY through this server. Backend is selected at
startup via `WAREHOUSE_BACKEND=postgres|databricks` — these tool signatures
never change, only the backend implementation swaps. Keep it clean (~100–150
lines with the official Python MCP SDK) — it's a portfolio artifact in its
own right, the thing you point to when you say "I authored a custom MCP
server".

Tools exposed:
    query(sql: str)                     -> read-only query
    write_table(table: str, rows: list) -> insert / upsert
    get_row_count(table: str)           -> used by the validator for reconciliation
"""

from __future__ import annotations

import os
from typing import Any

from mcp.server.mcpserver import MCPServer

from mcp_servers.warehouse_mcp.backends.base import WarehouseBackend

mcp = MCPServer("warehouse_mcp")


def _load_backend() -> WarehouseBackend:
    name = os.environ.get("WAREHOUSE_BACKEND", "postgres")
    if name == "postgres":
        from mcp_servers.warehouse_mcp.backends.postgres import PostgresBackend

        return PostgresBackend()
    if name == "databricks":
        from mcp_servers.warehouse_mcp.backends.databricks import DatabricksBackend

        return DatabricksBackend()
    raise ValueError(f"Unknown WAREHOUSE_BACKEND: {name!r} (expected postgres|databricks)")


_backend: WarehouseBackend | None = None


def _get_backend() -> WarehouseBackend:
    # Lazy so importing this module doesn't require a live backend — the
    # stub backends raise NotImplementedError from __init__ until Phase 1/2.
    global _backend
    if _backend is None:
        _backend = _load_backend()
    return _backend


@mcp.tool()
def query(sql: str) -> list[dict[str, Any]]:
    """Read-only query against the warehouse."""
    return _get_backend().query(sql)


@mcp.tool()
def write_table(table: str, rows: list[dict[str, Any]]) -> int:
    """Insert/upsert rows into a warehouse table."""
    return _get_backend().write_table(table, rows)


@mcp.tool()
def get_row_count(table: str) -> int:
    """Row count for a warehouse table, used by the validator for reconciliation."""
    return _get_backend().get_row_count(table)


def main() -> None:
    """Run the warehouse MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
