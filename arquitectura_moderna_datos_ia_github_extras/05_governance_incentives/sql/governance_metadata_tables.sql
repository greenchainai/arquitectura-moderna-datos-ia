CREATE SCHEMA IF NOT EXISTS governance;

CREATE TABLE IF NOT EXISTS governance.dataset_registry (
    dataset_id TEXT PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    domain TEXT NOT NULL,
    owner TEXT NOT NULL,
    description TEXT,
    refresh_frequency TEXT,
    criticality TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS governance.data_contract (
    contract_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL REFERENCES governance.dataset_registry(dataset_id),
    version TEXT NOT NULL,
    schema_definition JSONB NOT NULL,
    quality_rules JSONB,
    status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS governance.quality_rule (
    rule_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL REFERENCES governance.dataset_registry(dataset_id),
    rule_name TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    rule_expression TEXT NOT NULL,
    severity TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS governance.access_policy (
    policy_id TEXT PRIMARY KEY,
    dataset_id TEXT NOT NULL REFERENCES governance.dataset_registry(dataset_id),
    role_name TEXT NOT NULL,
    permission TEXT NOT NULL,
    condition TEXT
);
