CREATE SCHEMA IF NOT EXISTS vault;

CREATE TABLE IF NOT EXISTS vault.hub_shipment (
    shipment_hk TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL,
    load_datetime TIMESTAMP NOT NULL,
    record_source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vault.link_order_shipment (
    order_shipment_hk TEXT PRIMARY KEY,
    order_hk TEXT NOT NULL,
    shipment_hk TEXT NOT NULL,
    load_datetime TIMESTAMP NOT NULL,
    record_source TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS vault.sat_shipment_status (
    shipment_hk TEXT NOT NULL,
    load_datetime TIMESTAMP NOT NULL,
    shipment_status TEXT,
    planned_date DATE,
    actual_date DATE,
    record_source TEXT NOT NULL,
    hashdiff TEXT,
    PRIMARY KEY (shipment_hk, load_datetime)
);
