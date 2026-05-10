INSERT INTO staging.stg_tracking_events (
    tracking_event_id, shipment_id, event_type, event_timestamp,
    location, event_source, source_system, ingestion_batch_id, ingestion_timestamp
)
SELECT
    payload->>'tracking_event_id', payload->>'shipment_id', UPPER(TRIM(payload->>'event_type')),
    (payload->>'event_timestamp')::timestamp, TRIM(payload->>'location'),
    COALESCE(payload->>'event_source', source_system), source_system,
    ingestion_batch_id, ingestion_timestamp
FROM raw.raw_tracking_events
WHERE processing_status = 'PENDING'
ON CONFLICT (tracking_event_id)
DO UPDATE SET
    event_type = EXCLUDED.event_type,
    event_timestamp = EXCLUDED.event_timestamp,
    location = EXCLUDED.location,
    event_source = EXCLUDED.event_source,
    ingestion_batch_id = EXCLUDED.ingestion_batch_id,
    ingestion_timestamp = EXCLUDED.ingestion_timestamp;
