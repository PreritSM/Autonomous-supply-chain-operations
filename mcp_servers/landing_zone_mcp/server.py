"""landing_zone_mcp — MCP server wrapping the raw-file landing zone (Build Spec §7).

The ingestion agent reads incoming files and quarantines bad ones ONLY through
this server. Keep it clean (~100–150 lines with the official Python MCP SDK).

Tools exposed:
    list_new_files()                        -> files awaiting ingestion in data/landing/
    read_file(path: str)                    -> file contents
    move_to_quarantine(path: str, reason)   -> move a bad file out of the landing zone
"""

from __future__ import annotations

# from mcp.server.fastmcp import FastMCP
# mcp = FastMCP("landing_zone_mcp")


def main() -> None:
    """Run the landing-zone MCP server over stdio. TODO: implement per §7."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
