# Modelo conceptual logístico

```text
Customer 1 ──── N Order
Order 1 ──── N Shipment
Shipment 1 ──── N TrackingEvent
Shipment 1 ──── N Incident
Shipment N ──── 1 Carrier
Shipment N ──── 1 Route
Shipment N ──── 1 Warehouse
Shipment 1 ──── N Document
Shipment 1 ──── N EmissionRecord
```
