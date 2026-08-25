"""Warehouse backends behind the `warehouse_mcp` seam.

Selected at server startup via `WAREHOUSE_BACKEND=postgres|databricks`
(see CLAUDE.md's MCP-is-the-backend-abstraction-seam decision). `server.py`'s
tool signatures never change — only the backend implementation swaps.
"""

from __future__ import annotations
