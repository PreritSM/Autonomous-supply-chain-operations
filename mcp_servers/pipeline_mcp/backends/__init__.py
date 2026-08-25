"""Pipeline/transform-trigger backends behind the `pipeline_mcp` seam.

Selected at server startup via `PIPELINE_BACKEND=dbt|databricks` (ratified
2026-08-25, see Claude_Plan/DECISIONS.md). `server.py`'s tool signatures
never change — only the backend implementation swaps.
"""

from __future__ import annotations
