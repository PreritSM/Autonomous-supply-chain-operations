"""landing_zone_mcp — MCP server wrapping the raw-file landing zone (Build
Spec §7, backend seam per CLAUDE.md's "MCP is the backend abstraction"
decision).

The ingestion agent reads incoming files and quarantines bad ones ONLY
through this server. Backend is selected at startup via
`LANDING_ZONE_BACKEND=local_fs|uc_volume` — these tool signatures never
change, only the backend implementation swaps. Keep it clean (~100–150 lines
with the official Python MCP SDK).

Tools exposed:
    list_new_files()                        -> files awaiting ingestion in data/landing/
    read_file(path: str)                    -> file contents
    move_to_quarantine(path: str, reason)   -> move a bad file out of the landing zone
"""

from __future__ import annotations

import os

from mcp.server.mcpserver import MCPServer

from mcp_servers.landing_zone_mcp.backends.base import LandingZoneBackend

mcp = MCPServer("landing_zone_mcp")


def _load_backend() -> LandingZoneBackend:
    name = os.environ.get("LANDING_ZONE_BACKEND", "local_fs")
    if name == "local_fs":
        from mcp_servers.landing_zone_mcp.backends.local_fs import LocalFsBackend

        return LocalFsBackend()
    if name == "uc_volume":
        from mcp_servers.landing_zone_mcp.backends.uc_volume import UCVolumeBackend

        return UCVolumeBackend()
    raise ValueError(f"Unknown LANDING_ZONE_BACKEND: {name!r} (expected local_fs|uc_volume)")


_backend: LandingZoneBackend | None = None


def _get_backend() -> LandingZoneBackend:
    # Lazy so importing this module doesn't require a live backend — the
    # stub backends raise NotImplementedError from __init__ until Phase 1/2.
    global _backend
    if _backend is None:
        _backend = _load_backend()
    return _backend


@mcp.tool()
def list_new_files() -> list[str]:
    """Files awaiting ingestion in the landing zone."""
    return _get_backend().list_new_files()


@mcp.tool()
def read_file(path: str) -> bytes:
    """Contents of a landing-zone file."""
    return _get_backend().read_file(path)


@mcp.tool()
def move_to_quarantine(path: str, reason: str) -> None:
    """Move a bad file out of the landing zone, tagged with `reason`."""
    _get_backend().move_to_quarantine(path, reason)


def main() -> None:
    """Run the landing-zone MCP server over stdio."""
    mcp.run()


if __name__ == "__main__":
    main()
