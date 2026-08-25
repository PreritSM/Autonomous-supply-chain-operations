"""Postgres backend for `warehouse_mcp` — the default backend (Phase 1).

Reads connection details from POSTGRES_HOST/PORT/USER/PASSWORD/DB (see
.env.example). Implementation lands in Phase 1; Phase 0 only fixes the shape
of the seam.
"""

from __future__ import annotations

from typing import Any

from mcp_servers.warehouse_mcp.backends.base import WarehouseBackend


class PostgresBackend(WarehouseBackend):
    def __init__(self) -> None:
        raise NotImplementedError

    def query(self, sql: str) -> list[dict[str, Any]]:
        raise NotImplementedError

    def write_table(self, table: str, rows: list[dict[str, Any]]) -> int:
        raise NotImplementedError

    def get_row_count(self, table: str) -> int:
        raise NotImplementedError
