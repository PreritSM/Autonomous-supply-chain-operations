-- bi_agent_audit_log: one row per audit-log entry (§14.1).
-- Sourced from the audit_log list each agent appends to in PipelineState.
-- Columns: run_id, agent_name, timestamp, message, triggered_feedback_loop.
-- Power BI Page 3 (Agent Audit Trail) highlights triggered_feedback_loop rows —
-- this is what visibly proves the system is agentic. TODO: implement.
select
    1
where false
