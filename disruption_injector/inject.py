"""Disruption injector — the validation trick (Build Spec §8).

This is the single thing that makes the project *provable* rather than plausible.
It takes clean M5 data and deliberately corrupts a controlled, logged fraction of
it, returning both the corrupted frame and a ground-truth log of exactly which
rows/cells were touched. The readiness agent's catch rate is scored against that
log: ``detected ∩ actual / actual`` — a real precision/recall number.

The five disruption types map 1:1 to the ingestion agent's quality rules and the
``QualityIssue.issue_type`` categories in agents/state.py — keep them in sync.
"""

from __future__ import annotations

# import pandas as pd

DISRUPTION_TYPES = (
    "missing_values",   # null out a % of a column
    "duplicate_rows",   # re-insert existing rows
    "schema_drift",     # rename / add an unexpected column
    "out_of_range",     # negative prices, impossible quantities
    "type_corruption",  # numeric field becomes a string
)


def inject(df, disruption_type: str, rate: float, seed: int = 42):
    """Corrupt ``df`` and return ``(corrupted_df, ground_truth_issues)``.

    ``ground_truth_issues`` records exactly which rows/cells were touched — it is
    what the readiness agent is scored against. TODO: implement per §8.
    """
    raise NotImplementedError
