CREATE SCHEMA IF NOT EXISTS mart;

CREATE TABLE IF NOT EXISTS mart.dim_carrier (
    carrier_key BIGSERIAL PRIMARY KEY,
    carrier_id TEXT NOT NULL,
    carrier_name TEXT NOT NULL,
    carrier_type TEXT,
    country TEXT,
    service_level TEXT,
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS mart.fact_shipments (
    shipment_key BIGSERIAL PRIMARY KEY,
    shipment_id TEXT NOT NULL,
    customer_key BIGINT NOT NULL,
    carrier_key BIGINT NOT NULL,
    route_key BIGINT NOT NULL,
    origin_warehouse_key BIGINT,
    planned_date_key INT,
    actual_date_key INT,
    total_packages INT,
    delivery_delay_days INT,
    is_delivered_on_time BOOLEAN,
    co2_kg NUMERIC(12, 3),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
