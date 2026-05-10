CREATE SCHEMA IF NOT EXISTS decisioning;

CREATE TABLE IF NOT EXISTS decisioning.shipment_delay_prediction (
    prediction_id TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL,
    model_version TEXT NOT NULL,
    delay_risk_score NUMERIC(5,4) NOT NULL,
    predicted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    explanation JSONB
);

CREATE TABLE IF NOT EXISTS decisioning.route_risk_score (
    route_risk_id TEXT PRIMARY KEY,
    route_id TEXT NOT NULL,
    risk_score NUMERIC(5,4) NOT NULL,
    risk_reason TEXT,
    calculated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decisioning.recommended_action (
    recommendation_id TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL,
    recommendation_type TEXT NOT NULL,
    recommendation_text TEXT,
    requires_approval BOOLEAN NOT NULL DEFAULT TRUE,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decisioning.decision_log (
    decision_id TEXT PRIMARY KEY,
    recommendation_id TEXT REFERENCES decisioning.recommended_action(recommendation_id),
    shipment_id TEXT NOT NULL,
    decision_status TEXT NOT NULL,
    decided_by TEXT,
    decided_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    action_executed TEXT,
    evidence JSONB
);

CREATE TABLE IF NOT EXISTS decisioning.feedback_event (
    feedback_id TEXT PRIMARY KEY,
    decision_id TEXT REFERENCES decisioning.decision_log(decision_id),
    outcome TEXT NOT NULL,
    impact_metric JSONB,
    captured_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
