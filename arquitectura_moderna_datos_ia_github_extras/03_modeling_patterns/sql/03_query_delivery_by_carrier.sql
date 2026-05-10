SELECT
    c.carrier_name,
    d.year,
    d.month,
    COUNT(*) AS total_shipments,
    AVG(f.delivery_delay_days) AS avg_delay_days,
    SUM(f.co2_kg) AS total_co2_kg
FROM mart.fact_shipments f
JOIN mart.dim_carrier c ON f.carrier_key = c.carrier_key
JOIN mart.dim_date d ON f.actual_date_key = d.date_key
GROUP BY c.carrier_name, d.year, d.month
ORDER BY d.year, d.month, c.carrier_name;
