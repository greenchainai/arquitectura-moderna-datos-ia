SELECT DATE(ingestion_timestamp) AS ingestion_date, COUNT(*) AS total_events
FROM staging.stg_tracking_events
GROUP BY DATE(ingestion_timestamp)
ORDER BY ingestion_date DESC;

SELECT MAX(event_timestamp) AS last_tracking_event,
       CURRENT_TIMESTAMP - MAX(event_timestamp) AS delay
FROM staging.stg_tracking_events;
