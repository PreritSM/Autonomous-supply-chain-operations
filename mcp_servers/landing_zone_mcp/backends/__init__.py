"""Landing-zone backends behind the `landing_zone_mcp` seam.

Selected at server startup via `LANDING_ZONE_BACKEND=local_fs|uc_volume`
(see CLAUDE.md's MCP-is-the-backend-abstraction-seam decision). `server.py`'s
tool signatures never change — only the backend implementation swaps.
"""

from __future__ import annotations
