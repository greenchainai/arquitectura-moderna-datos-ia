CREATE TABLE mart.fact_shipments AS
SELECT
    s.shipment_id,
    dc.customer_key,
    dca.carrier_key,
    dr.route_key,
    dd_planned.date_key AS planned_date_key,
    dd_actual.date_key AS actual_date_key,
    s.total_packages,
    CASE WHEN s.actual_delivery_date IS NULL THEN NULL ELSE s.actual_delivery_date - s.planned_delivery_date END AS delivery_delay_days,
    CASE WHEN s.actual_delivery_date <= s.planned_delivery_date THEN TRUE ELSE FALSE END AS is_delivered_on_time,
    e.co2_kg
FROM staging.stg_shipments s
LEFT JOIN mart.dim_customer dc ON s.customer_id = dc.customer_id
LEFT JOIN mart.dim_carrier dca ON s.carrier_id = dca.carrier_id
LEFT JOIN mart.dim_route dr ON s.route_id = dr.route_id
LEFT JOIN mart.dim_date dd_planned ON s.planned_delivery_date = dd_planned.full_date
LEFT JOIN mart.dim_date dd_actual ON s.actual_delivery_date = dd_actual.full_date
LEFT JOIN staging.stg_emission_records e ON s.shipment_id = e.shipment_id;
