"""Local-filesystem backend for `landing_zone_mcp` — the default backend
(Phase 1), reading/writing under `data/landing/`.

Implementation lands in Phase 1; Phase 0 only fixes the shape of the seam.
"""

from __future__ import annotations

from mcp_servers.landing_zone_mcp.backends.base import LandingZoneBackend


class LocalFsBackend(LandingZoneBackend):
    def __init__(self) -> None:
        raise NotImplementedError

    def list_new_files(self) -> list[str]:
        raise NotImplementedError

    def read_file(self, path: str) -> bytes:
        raise NotImplementedError

    def move_to_quarantine(self, path: str, reason: str) -> None:
        raise NotImplementedError
