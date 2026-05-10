-- ============================================================
-- Book lab: Arquitectura Moderna de Datos e IA
-- Script: 01_create_schema_tables_indexes.sql
-- Dialect: PostgreSQL
-- Purpose: create operational logistics model + indexes.
--
-- Execute after creating the database:
--   psql -U postgres -d logistics_ai_lab -f sql/01_create_schema_tables_indexes.sql
-- ============================================================

CREATE SCHEMA IF NOT EXISTS logistics;
SET search_path TO logistics, public;

-- Useful extension for case-insensitive or fuzzy searches later if needed.
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ------------------------------------------------------------
-- Clean deployment for lab usage.
-- WARNING: drops all objects in schema logistics.
-- ------------------------------------------------------------
DROP TABLE IF EXISTS decision_log CASCADE;
DROP TABLE IF EXISTS emission_records CASCADE;
DROP TABLE IF EXISTS documents CASCADE;
DROP TABLE IF EXISTS sensor_readings CASCADE;
DROP TABLE IF EXISTS incidents CASCADE;
DROP TABLE IF EXISTS tracking_events CASCADE;
DROP TABLE IF EXISTS shipments CASCADE;
DROP TABLE IF EXISTS order_lines CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS routes CASCADE;
DROP TABLE IF EXISTS carriers CASCADE;
DROP TABLE IF EXISTS warehouses CASCADE;
DROP TABLE IF EXISTS partners CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- ------------------------------------------------------------
-- Master and partner data
-- ------------------------------------------------------------
CREATE TABLE customers (
    customer_id              BIGINT PRIMARY KEY,
    external_customer_code   VARCHAR(50) NOT NULL UNIQUE,
    customer_name            VARCHAR(200) NOT NULL,
    customer_segment         VARCHAR(50) NOT NULL,
    country                  VARCHAR(80) NOT NULL,
    city                     VARCHAR(120) NOT NULL,
    industry                 VARCHAR(120) NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE partners (
    partner_id               BIGINT PRIMARY KEY,
    partner_name             VARCHAR(200) NOT NULL,
    partner_type             VARCHAR(50) NOT NULL,
    country                  VARCHAR(80) NOT NULL,
    api_endpoint             TEXT,
    is_data_space_ready      BOOLEAN NOT NULL DEFAULT false,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_partners_type CHECK (partner_type IN ('carrier','customer','supplier','public_sector','data_provider'))
);

CREATE TABLE warehouses (
    warehouse_id             BIGINT PRIMARY KEY,
    warehouse_name           VARCHAR(200) NOT NULL,
    country                  VARCHAR(80) NOT NULL,
    city                     VARCHAR(120) NOT NULL,
    capacity_units           INTEGER NOT NULL,
    latitude                 NUMERIC(9,6),
    longitude                NUMERIC(9,6),
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE carriers (
    carrier_id               BIGINT PRIMARY KEY,
    partner_id               BIGINT REFERENCES partners(partner_id),
    carrier_name             VARCHAR(200) NOT NULL,
    carrier_type             VARCHAR(50) NOT NULL,
    country                  VARCHAR(80) NOT NULL,
    service_level            VARCHAR(50) NOT NULL,
    sustainability_score     NUMERIC(5,2) NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_carrier_type CHECK (carrier_type IN ('road','rail','air','sea','multimodal')),
    CONSTRAINT chk_service_level CHECK (service_level IN ('standard','express','premium','economy')),
    CONSTRAINT chk_sustainability_score CHECK (sustainability_score BETWEEN 0 AND 100)
);

CREATE TABLE routes (
    route_id                 BIGINT PRIMARY KEY,
    origin_warehouse_id      BIGINT NOT NULL REFERENCES warehouses(warehouse_id),
    destination_country      VARCHAR(80) NOT NULL,
    destination_city         VARCHAR(120) NOT NULL,
    distance_km              NUMERIC(10,2) NOT NULL,
    route_type               VARCHAR(50) NOT NULL,
    planned_transit_hours    NUMERIC(10,2) NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_route_type CHECK (route_type IN ('domestic','international','urban','regional','long_haul')),
    CONSTRAINT chk_route_distance CHECK (distance_km > 0)
);

-- ------------------------------------------------------------
-- Orders and shipments
-- ------------------------------------------------------------
CREATE TABLE orders (
    order_id                 BIGINT PRIMARY KEY,
    customer_id              BIGINT NOT NULL REFERENCES customers(customer_id),
    order_date               TIMESTAMPTZ NOT NULL,
    promised_delivery_date   TIMESTAMPTZ NOT NULL,
    order_status             VARCHAR(50) NOT NULL,
    sales_channel            VARCHAR(50) NOT NULL,
    currency                 CHAR(3) NOT NULL DEFAULT 'EUR',
    order_amount             NUMERIC(14,2) NOT NULL DEFAULT 0,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_order_status CHECK (order_status IN ('created','confirmed','allocated','shipped','delivered','cancelled','returned')),
    CONSTRAINT chk_sales_channel CHECK (sales_channel IN ('b2b','b2c','marketplace','edi','api'))
);

CREATE TABLE order_lines (
    order_line_id            BIGINT PRIMARY KEY,
    order_id                 BIGINT NOT NULL REFERENCES orders(order_id) ON DELETE CASCADE,
    sku                      VARCHAR(80) NOT NULL,
    product_category         VARCHAR(100) NOT NULL,
    quantity                 INTEGER NOT NULL,
    unit_price               NUMERIC(12,2) NOT NULL,
    weight_kg                NUMERIC(12,3) NOT NULL,
    volume_m3                NUMERIC(12,4) NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_order_line_qty CHECK (quantity > 0),
    CONSTRAINT chk_order_line_price CHECK (unit_price >= 0)
);

CREATE TABLE shipments (
    shipment_id              BIGINT PRIMARY KEY,
    order_id                 BIGINT NOT NULL REFERENCES orders(order_id),
    carrier_id               BIGINT NOT NULL REFERENCES carriers(carrier_id),
    route_id                 BIGINT NOT NULL REFERENCES routes(route_id),
    origin_warehouse_id      BIGINT NOT NULL REFERENCES warehouses(warehouse_id),
    destination_country      VARCHAR(80) NOT NULL,
    destination_city         VARCHAR(120) NOT NULL,
    planned_departure_ts     TIMESTAMPTZ NOT NULL,
    actual_departure_ts      TIMESTAMPTZ,
    planned_delivery_ts      TIMESTAMPTZ NOT NULL,
    actual_delivery_ts       TIMESTAMPTZ,
    shipment_status          VARCHAR(50) NOT NULL,
    total_weight_kg          NUMERIC(14,3) NOT NULL,
    total_volume_m3          NUMERIC(14,4) NOT NULL,
    delay_minutes            INTEGER NOT NULL DEFAULT 0,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_shipment_status CHECK (shipment_status IN ('created','in_transit','delivered','delayed','cancelled','returned')),
    CONSTRAINT chk_shipment_delay CHECK (delay_minutes >= 0)
);

CREATE TABLE tracking_events (
    tracking_event_id        BIGINT PRIMARY KEY,
    shipment_id              BIGINT NOT NULL REFERENCES shipments(shipment_id) ON DELETE CASCADE,
    event_timestamp          TIMESTAMPTZ NOT NULL,
    event_type               VARCHAR(80) NOT NULL,
    event_location           VARCHAR(200),
    latitude                 NUMERIC(9,6),
    longitude                NUMERIC(9,6),
    event_source             VARCHAR(80) NOT NULL,
    event_payload            JSONB,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_tracking_event_source CHECK (event_source IN ('tms','carrier_api','mobile_app','iot_gateway','manual'))
);

CREATE TABLE incidents (
    incident_id              BIGINT PRIMARY KEY,
    shipment_id              BIGINT NOT NULL REFERENCES shipments(shipment_id) ON DELETE CASCADE,
    incident_type            VARCHAR(80) NOT NULL,
    severity                 VARCHAR(30) NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL,
    resolved_at              TIMESTAMPTZ,
    incident_status          VARCHAR(50) NOT NULL,
    description              TEXT,
    CONSTRAINT chk_incident_severity CHECK (severity IN ('low','medium','high','critical')),
    CONSTRAINT chk_incident_status CHECK (incident_status IN ('open','in_progress','resolved','cancelled'))
);

-- ------------------------------------------------------------
-- IoT, documents, sustainability, decisions
-- ------------------------------------------------------------
CREATE TABLE sensor_readings (
    sensor_reading_id        BIGINT PRIMARY KEY,
    shipment_id              BIGINT REFERENCES shipments(shipment_id) ON DELETE SET NULL,
    warehouse_id             BIGINT REFERENCES warehouses(warehouse_id) ON DELETE SET NULL,
    route_id                 BIGINT REFERENCES routes(route_id) ON DELETE SET NULL,
    reading_ts               TIMESTAMPTZ NOT NULL,
    sensor_type              VARCHAR(80) NOT NULL,
    sensor_value             NUMERIC(14,4) NOT NULL,
    unit                     VARCHAR(30) NOT NULL,
    device_id                VARCHAR(100) NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_sensor_type CHECK (sensor_type IN ('temperature','humidity','vibration','fuel_level','door_open','gps_speed'))
);

CREATE TABLE documents (
    document_id              BIGINT PRIMARY KEY,
    shipment_id              BIGINT REFERENCES shipments(shipment_id) ON DELETE SET NULL,
    order_id                 BIGINT REFERENCES orders(order_id) ON DELETE SET NULL,
    incident_id              BIGINT REFERENCES incidents(incident_id) ON DELETE SET NULL,
    document_type            VARCHAR(80) NOT NULL,
    document_date            TIMESTAMPTZ NOT NULL,
    storage_path             TEXT NOT NULL,
    file_format              VARCHAR(20) NOT NULL,
    language_code            VARCHAR(10) NOT NULL DEFAULT 'es',
    extracted_text           TEXT,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_document_type CHECK (document_type IN ('invoice','delivery_note','proof_of_delivery','customs_form','incident_email','carrier_report')),
    CONSTRAINT chk_file_format CHECK (file_format IN ('pdf','docx','txt','html','jpg','png'))
);

CREATE TABLE emission_records (
    emission_id              BIGINT PRIMARY KEY,
    shipment_id              BIGINT NOT NULL REFERENCES shipments(shipment_id) ON DELETE CASCADE,
    route_id                 BIGINT NOT NULL REFERENCES routes(route_id),
    co2_kg                   NUMERIC(14,4) NOT NULL,
    fuel_type                VARCHAR(50) NOT NULL,
    calculation_method       VARCHAR(80) NOT NULL,
    calculated_at            TIMESTAMPTZ NOT NULL,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_co2 CHECK (co2_kg >= 0),
    CONSTRAINT chk_fuel_type CHECK (fuel_type IN ('diesel','electric','hybrid','rail_mix','air_freight','sea_freight'))
);

CREATE TABLE decision_log (
    decision_id              BIGINT PRIMARY KEY,
    shipment_id              BIGINT NOT NULL REFERENCES shipments(shipment_id) ON DELETE CASCADE,
    incident_id              BIGINT REFERENCES incidents(incident_id) ON DELETE SET NULL,
    decision_ts              TIMESTAMPTZ NOT NULL,
    decision_type            VARCHAR(80) NOT NULL,
    recommended_action       TEXT NOT NULL,
    decision_status          VARCHAR(50) NOT NULL,
    decided_by               VARCHAR(80) NOT NULL,
    confidence_score         NUMERIC(5,4),
    decision_reason          TEXT,
    action_taken             TEXT,
    outcome                  TEXT,
    created_at               TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT chk_decision_type CHECK (decision_type IN ('delay_risk','incident_escalation','route_change','carrier_change','customer_notification','co2_optimization')),
    CONSTRAINT chk_decision_status CHECK (decision_status IN ('recommended','accepted','rejected','executed','expired')),
    CONSTRAINT chk_confidence_score CHECK (confidence_score IS NULL OR confidence_score BETWEEN 0 AND 1)
);

-- ------------------------------------------------------------
-- Indexes: operational and analytical access paths
-- ------------------------------------------------------------
CREATE INDEX ix_customers_segment_country ON customers(customer_segment, country);
CREATE INDEX ix_partners_type_country ON partners(partner_type, country);
CREATE INDEX ix_warehouses_country_city ON warehouses(country, city);
CREATE INDEX ix_carriers_service_country ON carriers(service_level, country);
CREATE INDEX ix_routes_origin_destination ON routes(origin_warehouse_id, destination_country, destination_city);
CREATE INDEX ix_routes_type_distance ON routes(route_type, distance_km);

CREATE INDEX ix_orders_customer_date ON orders(customer_id, order_date DESC);
CREATE INDEX ix_orders_status_date ON orders(order_status, order_date DESC);
CREATE INDEX ix_orders_promised_delivery ON orders(promised_delivery_date);

CREATE INDEX ix_order_lines_order ON order_lines(order_id);
CREATE INDEX ix_order_lines_sku ON order_lines(sku);

CREATE INDEX ix_shipments_order ON shipments(order_id);
CREATE INDEX ix_shipments_carrier_status ON shipments(carrier_id, shipment_status);
CREATE INDEX ix_shipments_route_status ON shipments(route_id, shipment_status);
CREATE INDEX ix_shipments_planned_delivery ON shipments(planned_delivery_ts);
CREATE INDEX ix_shipments_actual_delivery ON shipments(actual_delivery_ts);
CREATE INDEX ix_shipments_delay_positive ON shipments(delay_minutes) WHERE delay_minutes > 0;

CREATE INDEX ix_tracking_events_shipment_ts ON tracking_events(shipment_id, event_timestamp);
CREATE INDEX ix_tracking_events_type_ts ON tracking_events(event_type, event_timestamp DESC);
CREATE INDEX ix_tracking_events_payload_gin ON tracking_events USING GIN(event_payload);

CREATE INDEX ix_incidents_shipment ON incidents(shipment_id);
CREATE INDEX ix_incidents_status_severity ON incidents(incident_status, severity);
CREATE INDEX ix_incidents_created ON incidents(created_at DESC);

CREATE INDEX ix_sensor_readings_shipment_ts ON sensor_readings(shipment_id, reading_ts DESC);
CREATE INDEX ix_sensor_readings_warehouse_ts ON sensor_readings(warehouse_id, reading_ts DESC);
CREATE INDEX ix_sensor_readings_route_ts ON sensor_readings(route_id, reading_ts DESC);
CREATE INDEX ix_sensor_readings_type_ts ON sensor_readings(sensor_type, reading_ts DESC);

CREATE INDEX ix_documents_shipment ON documents(shipment_id);
CREATE INDEX ix_documents_order ON documents(order_id);
CREATE INDEX ix_documents_incident ON documents(incident_id);
CREATE INDEX ix_documents_type_date ON documents(document_type, document_date DESC);

CREATE INDEX ix_emission_records_shipment ON emission_records(shipment_id);
CREATE INDEX ix_emission_records_route_calc ON emission_records(route_id, calculated_at DESC);
CREATE INDEX ix_emission_records_co2 ON emission_records(co2_kg DESC);

CREATE INDEX ix_decision_log_shipment_ts ON decision_log(shipment_id, decision_ts DESC);
CREATE INDEX ix_decision_log_type_status ON decision_log(decision_type, decision_status);
CREATE INDEX ix_decision_log_ts ON decision_log(decision_ts DESC);

-- ------------------------------------------------------------
-- Optional analytical views for first exploration
-- ------------------------------------------------------------
CREATE OR REPLACE VIEW v_shipments_enriched AS
SELECT
    s.shipment_id,
    s.order_id,
    o.customer_id,
    c.customer_name,
    c.customer_segment,
    s.carrier_id,
    ca.carrier_name,
    s.route_id,
    r.destination_country,
    r.destination_city,
    r.distance_km,
    s.shipment_status,
    s.planned_departure_ts,
    s.actual_departure_ts,
    s.planned_delivery_ts,
    s.actual_delivery_ts,
    s.delay_minutes,
    s.total_weight_kg,
    s.total_volume_m3,
    er.co2_kg,
    CASE WHEN s.delay_minutes > 0 THEN 1 ELSE 0 END AS is_delayed,
    CASE WHEN s.delay_minutes > 60 THEN 1 ELSE 0 END AS is_delayed_over_60m
FROM shipments s
JOIN orders o ON o.order_id = s.order_id
JOIN customers c ON c.customer_id = o.customer_id
JOIN carriers ca ON ca.carrier_id = s.carrier_id
JOIN routes r ON r.route_id = s.route_id
LEFT JOIN emission_records er ON er.shipment_id = s.shipment_id;

CREATE OR REPLACE VIEW v_delivery_kpis_daily AS
SELECT
    date_trunc('day', planned_delivery_ts)::date AS delivery_day,
    COUNT(*) AS shipments_count,
    SUM(CASE WHEN delay_minutes = 0 THEN 1 ELSE 0 END) AS on_time_shipments,
    SUM(CASE WHEN delay_minutes > 0 THEN 1 ELSE 0 END) AS delayed_shipments,
    ROUND(AVG(delay_minutes)::numeric, 2) AS avg_delay_minutes,
    ROUND(AVG(total_weight_kg)::numeric, 2) AS avg_weight_kg
FROM shipments
GROUP BY 1;
