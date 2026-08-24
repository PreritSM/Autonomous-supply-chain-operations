-- bi_forecast_vs_actual: wide, flat, one row per date × item × store (§14.1).
-- Columns: date, item_id, store_id, dept_id, cat_id, state_id, actual_demand,
-- forecast_demand, forecast_error, is_anomaly, disruption_run_id.
-- Power BI Page 1 (Forecast vs. Actual) reads this. Do NOT point Power BI at
-- fct_daily_demand directly. TODO: implement.
select
    1
where false
