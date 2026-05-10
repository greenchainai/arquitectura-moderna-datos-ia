CREATE SCHEMA IF NOT EXISTS staging;

CREATE TABLE IF NOT EXISTS staging.stg_tracking_events (
    tracking_event_id TEXT PRIMARY KEY,
    shipment_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,
    location TEXT,
    event_source TEXT,
    source_system TEXT NOT NULL,
    ingestion_batch_id TEXT NOT NULL,
    ingestion_timestamp TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_stg_tracking_events_shipment_id ON staging.stg_tracking_events(shipment_id);
CREATE INDEX IF NOT EXISTS idx_stg_tracking_events_event_timestamp ON staging.stg_tracking_events(event_timestamp);
