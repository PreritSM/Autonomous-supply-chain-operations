-- stg_sales: 1:1 typed view over raw M5 sales (Build Spec §6).
-- Unpivots the wide d_1..d_n unit-sales columns into (item/store, d_n, units)
-- long form so downstream layers can join to the calendar by day.
-- TODO: implement.
select
    1
where false
