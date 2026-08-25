"""Abstract interface every `landing_zone_mcp` backend implements.

`server.py` calls only these methods — it never knows which concrete backend
is behind them. Keeps `agents/` free of backend-conditional code (see
CLAUDE.md: `grep -rE "psycopg|databricks" agents/` must return nothing).
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class LandingZoneBackend(ABC):
    @abstractmethod
    def list_new_files(self) -> list[str]:
        """Files awaiting ingestion."""
        raise NotImplementedError

    @abstractmethod
    def read_file(self, path: str) -> bytes:
        """Raw file contents."""
        raise NotImplementedError

    @abstractmethod
    def move_to_quarantine(self, path: str, reason: str) -> None:
        """Move a bad file out of the landing zone."""
        raise NotImplementedError
