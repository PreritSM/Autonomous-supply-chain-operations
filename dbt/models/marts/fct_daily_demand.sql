-- fct_daily_demand: the mart the forecasting agent reads (Build Spec §6).
-- One row per date × item × store, with demand and the exogenous features
-- (price, events, SNAP) that must flow through to the model — most M5 series
-- are intermittent, so these can't be dropped.
-- TODO: implement.
select
    1
where false
