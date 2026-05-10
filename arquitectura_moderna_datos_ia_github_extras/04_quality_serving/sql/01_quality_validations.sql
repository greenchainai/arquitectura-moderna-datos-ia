SELECT s.shipment_id, s.order_id
FROM staging.stg_shipments s
LEFT JOIN staging.stg_orders o ON s.order_id = o.order_id
WHERE o.order_id IS NULL;

SELECT s.shipment_id, o.order_date, s.planned_delivery_date, s.actual_delivery_date
FROM staging.stg_shipments s
JOIN staging.stg_orders o ON s.order_id = o.order_id
WHERE s.actual_delivery_date < o.order_date;

SELECT shipment_status, COUNT(*) AS total_records
FROM staging.stg_shipments
WHERE shipment_status NOT IN ('CREATED', 'IN_TRANSIT', 'DELIVERED', 'DELAYED', 'CANCELLED')
GROUP BY shipment_status;
