SELECT shipment_id, event_type, event_timestamp, COUNT(*) AS duplicate_count
FROM staging.stg_tracking_events
GROUP BY shipment_id, event_type, event_timestamp
HAVING COUNT(*) > 1;

SELECT *
FROM staging.stg_tracking_events
WHERE event_timestamp > CURRENT_TIMESTAMP + INTERVAL '1 day';
