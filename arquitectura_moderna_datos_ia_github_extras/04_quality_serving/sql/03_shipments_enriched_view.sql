CREATE SCHEMA IF NOT EXISTS serving;

CREATE OR REPLACE VIEW serving.shipments_enriched AS
SELECT
    s.shipment_id, s.order_id, o.customer_id, c.customer_name,
    s.carrier_id, ca.carrier_name, s.route_id, r.origin, r.destination,
    s.shipment_status, s.planned_delivery_date, s.actual_delivery_date,
    CASE WHEN s.actual_delivery_date > s.planned_delivery_date THEN TRUE ELSE FALSE END AS is_delayed,
    CASE WHEN s.actual_delivery_date IS NOT NULL THEN s.actual_delivery_date - s.planned_delivery_date ELSE NULL END AS delay_days,
    COALESCE(i.total_incidents, 0) AS total_incidents,
    e.co2_kg
FROM staging.stg_shipments s
LEFT JOIN staging.stg_orders o ON s.order_id = o.order_id
LEFT JOIN staging.stg_customers c ON o.customer_id = c.customer_id
LEFT JOIN staging.stg_carriers ca ON s.carrier_id = ca.carrier_id
LEFT JOIN staging.stg_routes r ON s.route_id = r.route_id
LEFT JOIN (SELECT shipment_id, COUNT(*) AS total_incidents FROM staging.stg_incidents GROUP BY shipment_id) i ON s.shipment_id = i.shipment_id
LEFT JOIN staging.stg_emission_records e ON s.shipment_id = e.shipment_id;
