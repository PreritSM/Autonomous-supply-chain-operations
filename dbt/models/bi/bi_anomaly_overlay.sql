-- bi_anomaly_overlay: filtered view of bi_forecast_vs_actual where is_anomaly (§14.1).
-- Adds: anomaly_reason (z-score/IQR trigger detail), synthetic (true if this
-- anomaly was one deliberately injected for validation, false if the model
-- flagged it unprompted). Power BI Page 4. TODO: implement.
select
    1
where false
