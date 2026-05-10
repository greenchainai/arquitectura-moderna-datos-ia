#!/usr/bin/env python3
from __future__ import annotations

import argparse
import random
from datetime import date, datetime, timedelta
from pathlib import Path
import pandas as pd

COUNTRIES = ["ES", "FR", "DE", "IT", "PT"]
SEGMENTS = ["STANDARD", "PREMIUM", "STRATEGIC"]
ORDER_STATUS = ["CREATED", "CONFIRMED", "SHIPPED", "DELIVERED", "CANCELLED"]
SHIPMENT_STATUS = ["CREATED", "IN_TRANSIT", "DELIVERED", "DELAYED", "CANCELLED"]
EVENT_TYPES = ["CREATED", "PICKED_UP", "IN_TRANSIT", "ARRIVED_HUB", "OUT_FOR_DELIVERY", "DELIVERED", "DELAYED"]
INCIDENT_TYPES = ["CAPACITY", "CUSTOMS", "DAMAGE", "ADDRESS_ERROR", "WEATHER", "TRAFFIC"]
SEVERITIES = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]


def make_id(prefix: str, number: int) -> str:
    return f"{prefix}-{number:06d}"


def random_date(start: date, end: date) -> date:
    return start + timedelta(days=random.randint(0, (end - start).days))


def generate(output_dir: Path, n_orders: int, seed: int) -> None:
    random.seed(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    customers = [{"customer_id": make_id("CUS", i), "customer_name": f"Customer {i}", "customer_segment": random.choice(SEGMENTS), "country": random.choice(COUNTRIES), "industry": random.choice(["Retail", "Manufacturing", "Energy", "Construction"])} for i in range(1, 301)]
    carriers = [{"carrier_id": make_id("CAR", i), "carrier_name": f"Carrier {i}", "carrier_type": random.choice(["ROAD", "AIR", "SEA", "RAIL"]), "country": random.choice(COUNTRIES), "service_level": random.choice(["STANDARD", "EXPRESS", "ECONOMY"])} for i in range(1, 31)]
    warehouses = [{"warehouse_id": make_id("WH", i), "warehouse_name": f"Warehouse {i}", "location": random.choice(["Madrid", "Barcelona", "Valencia", "Zaragoza", "Sevilla"]), "capacity": random.randint(5000, 50000), "warehouse_type": random.choice(["REGIONAL", "NATIONAL", "CROSS_DOCK"])} for i in range(1, 21)]
    routes = [{"route_id": make_id("RTE", i), "origin": random.choice(["Madrid", "Barcelona", "Valencia", "Zaragoza"]), "destination": random.choice(["Paris", "Lisbon", "Berlin", "Milan", "Porto"]), "distance_km": round(random.uniform(80, 1800), 2), "route_type": random.choice(["DOMESTIC", "INTERNATIONAL"])} for i in range(1, 101)]
    partners = [{"partner_id": make_id("PAR", i), "partner_name": f"Partner {i}", "partner_type": random.choice(["CARRIER", "WAREHOUSE", "CUSTOMS", "DATA_PROVIDER"]), "country": random.choice(COUNTRIES)} for i in range(1, 21)]

    orders, order_lines, shipments, tracking_events = [], [], [], []
    incidents, sensor_readings, documents, emissions = [], [], [], []
    start, end = date(2026, 1, 1), date(2026, 5, 31)

    for i in range(1, n_orders + 1):
        order_id = make_id("ORD", i)
        customer = random.choice(customers)
        order_date = random_date(start, end)
        promised = order_date + timedelta(days=random.randint(1, 8))
        status = random.choices(ORDER_STATUS, weights=[5, 15, 15, 60, 5])[0]
        orders.append({"order_id": order_id, "customer_id": customer["customer_id"], "order_date": order_date.isoformat(), "promised_delivery_date": promised.isoformat(), "order_status": status})

        for line in range(1, random.randint(2, 5)):
            order_lines.append({"order_line_id": f"{order_id}-L{line}", "order_id": order_id, "product_code": f"SKU-{random.randint(1000, 9999)}", "quantity": random.randint(1, 20), "unit_price": round(random.uniform(10, 500), 2)})

        shipment_id = make_id("SHP", i)
        carrier, route, warehouse = random.choice(carriers), random.choice(routes), random.choice(warehouses)
        delay_days = random.choices([0, 1, 2, 3, 5, -1], weights=[55, 18, 10, 6, 3, 8])[0]
        actual = promised + timedelta(days=delay_days) if status != "CANCELLED" else None
        shipment_status = "DELIVERED" if status == "DELIVERED" else random.choice(SHIPMENT_STATUS)
        shipments.append({"shipment_id": shipment_id, "order_id": order_id, "carrier_id": carrier["carrier_id"], "route_id": route["route_id"], "origin_warehouse_id": warehouse["warehouse_id"], "destination_location": route["destination"], "shipment_status": shipment_status, "planned_delivery_date": promised.isoformat(), "actual_delivery_date": actual.isoformat() if actual else "", "total_packages": random.randint(1, 10)})

        base_ts = datetime.combine(order_date, datetime.min.time()) + timedelta(hours=8)
        for j, event_type in enumerate(EVENT_TYPES[:random.randint(3, 6)]):
            tracking_events.append({"tracking_event_id": f"TEV-{i:06d}-{j+1:02d}", "shipment_id": shipment_id, "event_timestamp": (base_ts + timedelta(hours=8*j)).isoformat(), "event_type": event_type, "location": random.choice([route["origin"], route["destination"], "Zaragoza Hub", "Madrid Hub"]), "event_source": random.choice(["tracking_api", "carrier_feed", "partner_feed"])})

        if random.random() < 0.22:
            created = base_ts + timedelta(hours=random.randint(10, 40))
            resolved = created + timedelta(hours=random.randint(2, 48)) if random.random() < 0.7 else None
            incidents.append({"incident_id": make_id("INC", len(incidents) + 1), "shipment_id": shipment_id, "incident_type": random.choice(INCIDENT_TYPES), "severity": random.choice(SEVERITIES), "created_at": created.isoformat(), "resolved_at": resolved.isoformat() if resolved else "", "incident_status": "RESOLVED" if resolved else "OPEN"})

        if random.random() < 0.35:
            sensor_readings.append({"sensor_reading_id": make_id("SEN", len(sensor_readings) + 1), "shipment_id": shipment_id, "sensor_type": random.choice(["TEMPERATURE", "HUMIDITY", "LOCATION_SIGNAL"]), "reading_value": round(random.uniform(2, 30), 4), "reading_unit": random.choice(["C", "%", "signal"]), "reading_timestamp": (base_ts + timedelta(hours=random.randint(1, 30))).isoformat()})

        documents.append({"document_id": make_id("DOC", len(documents) + 1), "related_entity_type": "SHIPMENT", "related_entity_id": shipment_id, "document_type": random.choice(["POD", "DELIVERY_NOTE", "INCIDENT_REPORT", "CUSTOMER_EMAIL"]), "document_date": order_date.isoformat(), "storage_path": f"/documents/shipments/{shipment_id}.pdf", "language": random.choice(["es", "en", "fr"])})
        emissions.append({"emission_id": make_id("EMI", len(emissions) + 1), "shipment_id": shipment_id, "route_id": route["route_id"], "co2_kg": round(float(route["distance_km"]) * random.uniform(0.08, 0.22), 3), "calculation_method": random.choice(["DISTANCE_FACTOR", "CARRIER_FACTOR", "ESTIMATED"]), "calculated_at": datetime.utcnow().isoformat()})

    tables = {"customers": customers, "partners": partners, "warehouses": warehouses, "carriers": carriers, "routes": routes, "orders": orders, "order_lines": order_lines, "shipments": shipments, "tracking_events": tracking_events, "incidents": incidents, "sensor_readings": sensor_readings, "documents": documents, "emission_records": emissions}
    for name, rows in tables.items():
        pd.DataFrame(rows).to_csv(output_dir / f"{name}.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="data/generated")
    parser.add_argument("--n-orders", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    generate(Path(args.output_dir), args.n_orders, args.seed)
