"""Abstract interface every `pipeline_mcp` backend implements.

`server.py` calls only these methods — it never knows which concrete backend
is behind them. Keeps `transformation_agent.py` free of backend-conditional
code (see CLAUDE.md: `grep -rE "psycopg|databricks" agents/` must return
nothing).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class PipelineBackend(ABC):
    @abstractmethod
    def run_transform(
        self, layer: str, full_refresh: bool, tables: list[str] | None
    ) -> dict[str, Any]:
        """Trigger the transform for this backend. Returns run status incl. run_id.

        Postgres: shells out to `dbt run`/`dbt test`.
        Databricks: triggers a Lakeflow Declarative Pipeline update.
        """
        raise NotImplementedError

    @abstractmethod
    def get_quality_metrics(self, run_id: str) -> dict[str, Any]:
        """Quality metrics for a prior run.

        Postgres: dbt test results.
        Databricks: `event_log(<pipeline_id>) WHERE event_type='flow_progress'`
        violation metrics.
        """
        raise NotImplementedError
