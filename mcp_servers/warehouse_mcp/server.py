"""warehouse_mcp — MCP server wrapping the Postgres warehouse (Build Spec §7).

Agents reach the warehouse ONLY through this server. Keep it clean (~100–150
lines with the official Python MCP SDK) — it's a portfolio artifact in its own
right, the thing you point to when you say "I authored a custom MCP server".

Tools exposed:
    query(sql: str)                     -> read-only query
    write_table(table: str, rows: list) -> insert / upsert
    get_row_count(table: str)           -> used by the validator for reconciliation
"""

from __future__ import annotations

# from mcp.server.fastmcp import FastMCP
# mcp = FastMCP("warehouse_mcp")


def main() -> None:
    """Run the warehouse MCP server over stdio. TODO: implement per §7."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
