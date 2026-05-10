-- Quick validation after loading synthetic data.
SET search_path TO logistics, public;

SELECT 'customers' AS table_name, COUNT(*) FROM customers
UNION ALL SELECT 'partners', COUNT(*) FROM partners
UNION ALL SELECT 'warehouses', COUNT(*) FROM warehouses
UNION ALL SELECT 'carriers', COUNT(*) FROM carriers
UNION ALL SELECT 'routes', COUNT(*) FROM routes
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_lines', COUNT(*) FROM order_lines
UNION ALL SELECT 'shipments', COUNT(*) FROM shipments
UNION ALL SELECT 'tracking_events', COUNT(*) FROM tracking_events
UNION ALL SELECT 'incidents', COUNT(*) FROM incidents
UNION ALL SELECT 'sensor_readings', COUNT(*) FROM sensor_readings
UNION ALL SELECT 'documents', COUNT(*) FROM documents
UNION ALL SELECT 'emission_records', COUNT(*) FROM emission_records
UNION ALL SELECT 'decision_log', COUNT(*) FROM decision_log
ORDER BY table_name;

SELECT * FROM v_delivery_kpis_daily ORDER BY delivery_day DESC LIMIT 10;
