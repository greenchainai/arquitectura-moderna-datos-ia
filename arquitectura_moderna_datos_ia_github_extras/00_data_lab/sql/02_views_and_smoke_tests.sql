CREATE OR REPLACE VIEW logistics.v_shipments_enriched AS
SELECT
    s.shipment_id,
    s.order_id,
    o.customer_id,
    c.customer_name,
    c.customer_segment,
    s.carrier_id,
    ca.carrier_name,
    s.route_id,
    r.origin,
    r.destination,
    r.distance_km,
    s.shipment_status,
    s.planned_delivery_date,
    s.actual_delivery_date,
    CASE
        WHEN s.actual_delivery_date IS NOT NULL
         AND s.actual_delivery_date <= s.planned_delivery_date THEN TRUE
        WHEN s.actual_delivery_date IS NULL THEN NULL
        ELSE FALSE
    END AS is_delivered_on_time,
    CASE
        WHEN s.actual_delivery_date IS NOT NULL THEN
            s.actual_delivery_date - s.planned_delivery_date
        ELSE NULL
    END AS delivery_delay_days
FROM logistics.shipments s
JOIN logistics.orders o ON s.order_id = o.order_id
JOIN logistics.customers c ON o.customer_id = c.customer_id
JOIN logistics.carriers ca ON s.carrier_id = ca.carrier_id
JOIN logistics.routes r ON s.route_id = r.route_id;

CREATE OR REPLACE VIEW logistics.v_delivery_kpis_daily AS
SELECT
    actual_delivery_date AS delivery_date,
    carrier_id,
    route_id,
    COUNT(*) AS total_deliveries,
    SUM(CASE WHEN actual_delivery_date <= planned_delivery_date THEN 1 ELSE 0 END) AS on_time_deliveries,
    SUM(CASE WHEN actual_delivery_date > planned_delivery_date THEN 1 ELSE 0 END) AS delayed_deliveries,
    ROUND(
        SUM(CASE WHEN actual_delivery_date <= planned_delivery_date THEN 1 ELSE 0 END)::NUMERIC
        / NULLIF(COUNT(*), 0),
        4
    ) AS on_time_delivery_rate
FROM logistics.shipments
WHERE actual_delivery_date IS NOT NULL
GROUP BY actual_delivery_date, carrier_id, route_id;

SELECT 'customers' AS table_name, COUNT(*) FROM logistics.customers
UNION ALL SELECT 'orders', COUNT(*) FROM logistics.orders
UNION ALL SELECT 'shipments', COUNT(*) FROM logistics.shipments
UNION ALL SELECT 'tracking_events', COUNT(*) FROM logistics.tracking_events
UNION ALL SELECT 'incidents', COUNT(*) FROM logistics.incidents
UNION ALL SELECT 'emission_records', COUNT(*) FROM logistics.emission_records;
