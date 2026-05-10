SELECT
    tracking_event_id,
    shipment_id,
    UPPER(TRIM(event_type)) AS event_type,
    event_timestamp,
    location,
    event_source,
    ingestion_batch_id,
    ingestion_timestamp
FROM {{ source('raw', 'tracking_events') }}
WHERE tracking_event_id IS NOT NULL
  AND shipment_id IS NOT NULL
  AND event_timestamp IS NOT NULL
