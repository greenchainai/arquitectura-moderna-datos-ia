CREATE SCHEMA IF NOT EXISTS logistics;

CREATE TABLE IF NOT EXISTS logistics.customers (
    customer_id TEXT PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_segment TEXT NOT NULL,
    country TEXT NOT NULL,
    industry TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logistics.partners (
    partner_id TEXT PRIMARY KEY,
    partner_name TEXT NOT NULL,
    partner_type TEXT NOT NULL,
    country TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logistics.warehouses (
    warehouse_id TEXT PRIMARY KEY,
    warehouse_name TEXT NOT NULL,
    location TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    warehouse_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS logistics.carriers (
    carrier_id TEXT PRIMARY KEY,
    carrier_name TEXT NOT NULL,
    carrier_type TEXT NOT NULL,
    country TEXT NOT NULL,
    service_level TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS logistics.routes (
    route_id TEXT PRIMARY KEY,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    distance_km NUMERIC(12,2) NOT NULL,
    route_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS logistics.orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES logistics.customers(customer_id),
    order_date DATE NOT NULL,
    promised_delivery_date DATE NOT NULL,
    order_status TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logistics.order_lines (
    order_line_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL REFERENCES logistics.orders(order_id),
    product_code TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS logistics.shipments (
    shipment_id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL REFERENCES logistics.orders(order_id),
    carrier_id TEXT NOT NULL REFERENCES logistics.carriers(carrier_id),
    route_id TEXT NOT NULL REFERENCES logistics.routes(route_id),
    origin_warehouse_id TEXT NOT NULL REFERENCES logistics.warehouses(warehouse_id),
    destination_location TEXT NOT NULL,
    shipment_status TEXT NOT NULL,
    planned_delivery_date DATE NOT NULL,
    actual_delivery_date DATE,
    total_packages INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS logistics.tracking_events (
    tracking_event_id TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL REFERENCES logistics.shipments(shipment_id),
    event_timestamp TIMESTAMP NOT NULL,
    event_type TEXT NOT NULL,
    location TEXT,
    event_source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS logistics.incidents (
    incident_id TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL REFERENCES logistics.shipments(shipment_id),
    incident_type TEXT NOT NULL,
    severity TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    incident_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS logistics.sensor_readings (
    sensor_reading_id TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL REFERENCES logistics.shipments(shipment_id),
    sensor_type TEXT NOT NULL,
    reading_value NUMERIC(12,4) NOT NULL,
    reading_unit TEXT NOT NULL,
    reading_timestamp TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS logistics.documents (
    document_id TEXT PRIMARY KEY,
    related_entity_type TEXT NOT NULL,
    related_entity_id TEXT NOT NULL,
    document_type TEXT NOT NULL,
    document_date DATE NOT NULL,
    storage_path TEXT NOT NULL,
    language TEXT DEFAULT 'es'
);

CREATE TABLE IF NOT EXISTS logistics.emission_records (
    emission_id TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL REFERENCES logistics.shipments(shipment_id),
    route_id TEXT NOT NULL REFERENCES logistics.routes(route_id),
    co2_kg NUMERIC(12,3) NOT NULL,
    calculation_method TEXT NOT NULL,
    calculated_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS logistics.decision_log (
    decision_id TEXT PRIMARY KEY,
    shipment_id TEXT REFERENCES logistics.shipments(shipment_id),
    decision_type TEXT NOT NULL,
    recommendation TEXT,
    decision_status TEXT NOT NULL,
    decided_by TEXT,
    decided_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    outcome TEXT,
    feedback_score NUMERIC(5,2)
);

CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON logistics.orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_shipments_order_id ON logistics.shipments(order_id);
CREATE INDEX IF NOT EXISTS idx_shipments_carrier_id ON logistics.shipments(carrier_id);
CREATE INDEX IF NOT EXISTS idx_shipments_route_id ON logistics.shipments(route_id);
CREATE INDEX IF NOT EXISTS idx_tracking_events_shipment_id ON logistics.tracking_events(shipment_id);
CREATE INDEX IF NOT EXISTS idx_tracking_events_timestamp ON logistics.tracking_events(event_timestamp);
CREATE INDEX IF NOT EXISTS idx_incidents_shipment_id ON logistics.incidents(shipment_id);
CREATE INDEX IF NOT EXISTS idx_emission_records_shipment_id ON logistics.emission_records(shipment_id);
