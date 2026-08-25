"""Abstract interface every `warehouse_mcp` backend implements.

`server.py` calls only these methods — it never knows which concrete backend
is behind them. Keeps `agents/` free of backend-conditional code (see
CLAUDE.md: `grep -rE "psycopg|databricks" agents/` must return nothing).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class WarehouseBackend(ABC):
    @abstractmethod
    def query(self, sql: str) -> list[dict[str, Any]]:
        """Read-only query. Raise if `sql` is not a SELECT."""
        raise NotImplementedError

    @abstractmethod
    def write_table(self, table: str, rows: list[dict[str, Any]]) -> int:
        """Insert/upsert `rows` into `table`. Returns rows written."""
        raise NotImplementedError

    @abstractmethod
    def get_row_count(self, table: str) -> int:
        """Used by the validator agent for row-count reconciliation."""
        raise NotImplementedError
