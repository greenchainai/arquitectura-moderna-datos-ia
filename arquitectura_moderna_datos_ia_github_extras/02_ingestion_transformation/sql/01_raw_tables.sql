CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.raw_tracking_events (
    raw_event_id BIGSERIAL PRIMARY KEY,
    source_system TEXT NOT NULL,
    source_file_name TEXT,
    ingestion_batch_id TEXT NOT NULL,
    ingestion_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payload JSONB NOT NULL,
    payload_hash TEXT,
    processing_status TEXT DEFAULT 'PENDING'
);
