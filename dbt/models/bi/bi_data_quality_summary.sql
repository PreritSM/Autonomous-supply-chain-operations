-- bi_data_quality_summary: one row per (disruption_run_id, type, rate) (§14.1).
-- Columns: disruption_run_id, disruption_type, disruption_rate, rows_injected,
-- rows_caught, catch_rate, false_quarantine_count, false_quarantine_rate.
-- The headline metric made visual — Power BI Page 2. Aggregated by the eval
-- harness before landing in the warehouse. TODO: implement.
select
    1
where false
