CREATE OR REPLACE VIEW serving.delivery_kpis_daily AS
SELECT
    actual_delivery_date AS delivery_date,
    carrier_id,
    route_id,
    COUNT(*) AS total_deliveries,
    SUM(CASE WHEN actual_delivery_date <= planned_delivery_date THEN 1 ELSE 0 END) AS on_time_deliveries,
    SUM(CASE WHEN actual_delivery_date > planned_delivery_date THEN 1 ELSE 0 END) AS delayed_deliveries,
    ROUND(SUM(CASE WHEN actual_delivery_date <= planned_delivery_date THEN 1 ELSE 0 END)::numeric / NULLIF(COUNT(*), 0), 4) AS on_time_delivery_rate
FROM staging.stg_shipments
WHERE actual_delivery_date IS NOT NULL
GROUP BY actual_delivery_date, carrier_id, route_id;
