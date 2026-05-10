INSERT INTO vault.hub_shipment (shipment_hk, shipment_id, load_datetime, record_source)
SELECT DISTINCT md5(shipment_id), shipment_id, CURRENT_TIMESTAMP, source_system
FROM staging.stg_shipments
ON CONFLICT (shipment_hk) DO NOTHING;

INSERT INTO vault.link_order_shipment (order_shipment_hk, order_hk, shipment_hk, load_datetime, record_source)
SELECT DISTINCT
    md5(o.order_id || '-' || s.shipment_id),
    md5(o.order_id),
    md5(s.shipment_id),
    CURRENT_TIMESTAMP,
    s.source_system
FROM staging.stg_shipments s
JOIN staging.stg_orders o ON s.order_id = o.order_id
ON CONFLICT (order_shipment_hk) DO NOTHING;

INSERT INTO vault.sat_shipment_status (shipment_hk, load_datetime, shipment_status, planned_date, actual_date, record_source, hashdiff)
SELECT
    md5(shipment_id),
    CURRENT_TIMESTAMP,
    shipment_status,
    planned_delivery_date,
    actual_delivery_date,
    source_system,
    md5(COALESCE(shipment_status, '') || COALESCE(planned_delivery_date::text, '') || COALESCE(actual_delivery_date::text, ''))
FROM staging.stg_shipments;
