"""
Synthetic data generator for the logistics case study.

This module creates a coherent operational data model for the book:
Arquitectura Moderna de Datos e IA.

The generated entities are designed to be useful for:
- ingestion examples
- ETL/ELT examples
- dimensional modelling
- Data Vault examples
- quality and governance examples
- AI/RAG examples
- agents and decision intelligence examples

No external Faker dependency is required. The generator uses pandas + numpy only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class GenerationConfig:
    seed: int = 42
    n_customers: int = 500
    n_partners: int = 30
    n_warehouses: int = 12
    n_carriers: int = 15
    n_routes: int = 80
    n_orders: int = 5000
    start_date: str = "2025-01-01"
    end_date: str = "2026-04-30"


TABLE_ORDER = [
    "customers",
    "partners",
    "warehouses",
    "carriers",
    "routes",
    "orders",
    "order_lines",
    "shipments",
    "tracking_events",
    "incidents",
    "sensor_readings",
    "documents",
    "emission_records",
    "decision_log",
]

COUNTRIES_CITIES = {
    "Spain": ["Madrid", "Barcelona", "Valencia", "Seville", "Bilbao", "Zaragoza", "Malaga"],
    "France": ["Paris", "Lyon", "Marseille", "Toulouse", "Lille"],
    "Germany": ["Berlin", "Hamburg", "Munich", "Frankfurt", "Cologne"],
    "Italy": ["Rome", "Milan", "Turin", "Bologna", "Naples"],
    "Portugal": ["Lisbon", "Porto", "Braga", "Coimbra"],
    "Netherlands": ["Amsterdam", "Rotterdam", "Utrecht", "Eindhoven"],
}

CUSTOMER_SEGMENTS = ["enterprise", "mid_market", "sme", "public_sector"]
INDUSTRIES = ["retail", "manufacturing", "pharma", "food", "electronics", "automotive", "public_sector"]
SALES_CHANNELS = ["b2b", "b2c", "marketplace", "edi", "api"]
PRODUCT_CATEGORIES = ["electronics", "food", "textile", "industrial", "pharma", "spare_parts", "furniture"]
INCIDENT_TYPES = ["weather", "traffic", "customs", "vehicle_breakdown", "missing_document", "warehouse_delay", "damaged_goods"]
EVENT_TYPES_BASE = ["created", "picked_up", "departed_warehouse", "in_transit", "arrived_hub", "out_for_delivery", "delivered"]
DOC_TYPES = ["invoice", "delivery_note", "proof_of_delivery", "customs_form", "incident_email", "carrier_report"]
FUEL_BY_CARRIER_TYPE = {
    "road": ["diesel", "hybrid", "electric"],
    "rail": ["rail_mix", "electric"],
    "air": ["air_freight"],
    "sea": ["sea_freight"],
    "multimodal": ["diesel", "rail_mix", "hybrid"],
}


def _rng(config: GenerationConfig) -> np.random.Generator:
    return np.random.default_rng(config.seed)


def _parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value).replace(tzinfo=timezone.utc)


def _random_dt(rng: np.random.Generator, start: datetime, end: datetime) -> datetime:
    seconds = int((end - start).total_seconds())
    return start + timedelta(seconds=int(rng.integers(0, max(seconds, 1))))


def _choice(rng: np.random.Generator, values: List[str]) -> str:
    return str(values[int(rng.integers(0, len(values)))])


def _country_city(rng: np.random.Generator) -> Tuple[str, str]:
    country = _choice(rng, list(COUNTRIES_CITIES.keys()))
    city = _choice(rng, COUNTRIES_CITIES[country])
    return country, city


def _round(value: float, decimals: int = 2) -> float:
    return round(float(value), decimals)


def _iso(dt: datetime) -> str:
    # PostgreSQL and pandas parse this reliably.
    return dt.isoformat()


def generate_customers(config: GenerationConfig, rng: np.random.Generator) -> pd.DataFrame:
    prefixes = ["Iber", "Euro", "Nexa", "Trans", "Green", "Nova", "Atlas", "Prime", "North", "Blue"]
    suffixes = ["Logistics", "Retail", "Foods", "Systems", "Industries", "Health", "Motors", "Group", "Solutions"]
    rows = []
    for i in range(1, config.n_customers + 1):
        country, city = _country_city(rng)
        rows.append({
            "customer_id": i,
            "external_customer_code": f"CUST-{i:06d}",
            "customer_name": f"{_choice(rng, prefixes)} {_choice(rng, suffixes)} {i}",
            "customer_segment": _choice(rng, CUSTOMER_SEGMENTS),
            "country": country,
            "city": city,
            "industry": _choice(rng, INDUSTRIES),
            "created_at": _iso(_parse_dt(config.start_date) - timedelta(days=int(rng.integers(30, 365)))),
        })
    return pd.DataFrame(rows)


def generate_partners(config: GenerationConfig, rng: np.random.Generator) -> pd.DataFrame:
    partner_types = ["carrier", "carrier", "carrier", "supplier", "data_provider", "public_sector", "customer"]
    rows = []
    for i in range(1, config.n_partners + 1):
        country, _ = _country_city(rng)
        ptype = _choice(rng, partner_types)
        rows.append({
            "partner_id": i,
            "partner_name": f"Partner {ptype.title()} {i:03d}",
            "partner_type": ptype,
            "country": country,
            "api_endpoint": f"https://api.partner-{i:03d}.example.com/v1" if rng.random() < 0.75 else "",
            "is_data_space_ready": bool(rng.random() < 0.25),
            "created_at": _iso(_parse_dt(config.start_date) - timedelta(days=int(rng.integers(20, 600)))),
        })
    return pd.DataFrame(rows)


def generate_warehouses(config: GenerationConfig, rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for i in range(1, config.n_warehouses + 1):
        country, city = _country_city(rng)
        rows.append({
            "warehouse_id": i,
            "warehouse_name": f"WH-{city.upper().replace(' ', '-')}-{i:02d}",
            "country": country,
            "city": city,
            "capacity_units": int(rng.integers(5000, 80000)),
            "latitude": _round(rng.uniform(36.0, 53.0), 6),
            "longitude": _round(rng.uniform(-9.0, 15.0), 6),
            "created_at": _iso(_parse_dt(config.start_date) - timedelta(days=int(rng.integers(200, 1000)))),
        })
    return pd.DataFrame(rows)


def generate_carriers(config: GenerationConfig, rng: np.random.Generator, partners: pd.DataFrame) -> pd.DataFrame:
    carrier_types = ["road", "road", "road", "rail", "air", "sea", "multimodal"]
    service_levels = ["standard", "express", "premium", "economy"]
    carrier_partner_ids = partners.loc[partners["partner_type"].eq("carrier"), "partner_id"].tolist()
    if not carrier_partner_ids:
        carrier_partner_ids = partners["partner_id"].tolist()
    rows = []
    for i in range(1, config.n_carriers + 1):
        country, _ = _country_city(rng)
        rows.append({
            "carrier_id": i,
            "partner_id": int(rng.choice(carrier_partner_ids)) if rng.random() < 0.8 else "",
            "carrier_name": f"Carrier {i:03d}",
            "carrier_type": _choice(rng, carrier_types),
            "country": country,
            "service_level": _choice(rng, service_levels),
            "sustainability_score": _round(rng.uniform(35, 98), 2),
            "created_at": _iso(_parse_dt(config.start_date) - timedelta(days=int(rng.integers(100, 900)))),
        })
    return pd.DataFrame(rows)


def generate_routes(config: GenerationConfig, rng: np.random.Generator, warehouses: pd.DataFrame) -> pd.DataFrame:
    route_types = ["domestic", "international", "urban", "regional", "long_haul"]
    rows = []
    for i in range(1, config.n_routes + 1):
        origin_wh = warehouses.sample(n=1, random_state=int(rng.integers(0, 1_000_000))).iloc[0]
        dest_country, dest_city = _country_city(rng)
        route_type = _choice(rng, route_types)
        if route_type == "urban":
            distance = rng.uniform(5, 60)
        elif route_type == "regional":
            distance = rng.uniform(60, 400)
        elif route_type == "domestic":
            distance = rng.uniform(150, 900)
        elif route_type == "international":
            distance = rng.uniform(500, 2200)
        else:
            distance = rng.uniform(1000, 4500)
        planned_hours = distance / rng.uniform(45, 75) + rng.uniform(1, 12)
        rows.append({
            "route_id": i,
            "origin_warehouse_id": int(origin_wh["warehouse_id"]),
            "destination_country": dest_country,
            "destination_city": dest_city,
            "distance_km": _round(distance, 2),
            "route_type": route_type,
            "planned_transit_hours": _round(planned_hours, 2),
            "created_at": _iso(_parse_dt(config.start_date) - timedelta(days=int(rng.integers(100, 800)))),
        })
    return pd.DataFrame(rows)


def generate_orders_and_lines(config: GenerationConfig, rng: np.random.Generator, customers: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    start = _parse_dt(config.start_date)
    end = _parse_dt(config.end_date)
    orders_rows = []
    lines_rows = []
    line_id = 1
    for order_id in range(1, config.n_orders + 1):
        order_date = _random_dt(rng, start, end - timedelta(days=5))
        promised = order_date + timedelta(days=int(rng.integers(2, 12)), hours=int(rng.integers(0, 12)))
        customer_id = int(rng.integers(1, config.n_customers + 1))
        status = _choice(rng, ["created", "confirmed", "allocated", "shipped", "delivered", "delivered", "delivered", "cancelled", "returned"])
        n_lines = int(rng.integers(1, 6))
        order_amount = 0.0
        for _ in range(n_lines):
            qty = int(rng.integers(1, 20))
            unit_price = _round(rng.uniform(5, 700), 2)
            weight = _round(rng.uniform(0.1, 45.0) * qty, 3)
            volume = _round(rng.uniform(0.002, 0.25) * qty, 4)
            order_amount += qty * unit_price
            lines_rows.append({
                "order_line_id": line_id,
                "order_id": order_id,
                "sku": f"SKU-{int(rng.integers(10000, 99999))}",
                "product_category": _choice(rng, PRODUCT_CATEGORIES),
                "quantity": qty,
                "unit_price": unit_price,
                "weight_kg": weight,
                "volume_m3": volume,
                "created_at": _iso(order_date + timedelta(minutes=int(rng.integers(1, 180)))),
            })
            line_id += 1
        orders_rows.append({
            "order_id": order_id,
            "customer_id": customer_id,
            "order_date": _iso(order_date),
            "promised_delivery_date": _iso(promised),
            "order_status": status,
            "sales_channel": _choice(rng, SALES_CHANNELS),
            "currency": "EUR",
            "order_amount": _round(order_amount, 2),
            "created_at": _iso(order_date),
        })
    return pd.DataFrame(orders_rows), pd.DataFrame(lines_rows)


def generate_shipments(config: GenerationConfig, rng: np.random.Generator, orders: pd.DataFrame, order_lines: pd.DataFrame, carriers: pd.DataFrame, routes: pd.DataFrame) -> pd.DataFrame:
    line_totals = order_lines.groupby("order_id").agg(total_weight_kg=("weight_kg", "sum"), total_volume_m3=("volume_m3", "sum")).reset_index()
    orders_enriched = orders.merge(line_totals, on="order_id", how="left")
    route_lookup = routes.set_index("route_id").to_dict("index")
    end = _parse_dt(config.end_date)
    rows = []
    for i, row in orders_enriched.iterrows():
        shipment_id = int(row["order_id"])
        route_id = int(rng.integers(1, config.n_routes + 1))
        route = route_lookup[route_id]
        carrier_id = int(rng.integers(1, config.n_carriers + 1))
        order_date = datetime.fromisoformat(str(row["order_date"]))
        planned_departure = order_date + timedelta(hours=int(rng.integers(6, 72)))
        planned_delivery = planned_departure + timedelta(hours=float(route["planned_transit_hours"]))
        # Delay distribution: most shipments on-time, a few large delays.
        delay_probability = 0.22
        if route["route_type"] in ["international", "long_haul"]:
            delay_probability += 0.12
        is_delayed = rng.random() < delay_probability
        delay_minutes = int(max(0, rng.gamma(2.0, 55.0))) if is_delayed else 0
        depart_variance = int(rng.normal(0, 25))
        actual_departure = planned_departure + timedelta(minutes=depart_variance)
        actual_delivery = planned_delivery + timedelta(minutes=delay_minutes)
        if str(row["order_status"]) == "cancelled":
            status = "cancelled"
            actual_departure_out = ""
            actual_delivery_out = ""
            delay_minutes = 0
        elif actual_delivery > end and rng.random() < 0.65:
            status = "in_transit"
            actual_departure_out = _iso(actual_departure)
            actual_delivery_out = ""
        elif delay_minutes > 0:
            status = "delayed" if delay_minutes > 60 else "delivered"
            actual_departure_out = _iso(actual_departure)
            actual_delivery_out = _iso(actual_delivery)
        else:
            status = "delivered"
            actual_departure_out = _iso(actual_departure)
            actual_delivery_out = _iso(actual_delivery)
        rows.append({
            "shipment_id": shipment_id,
            "order_id": int(row["order_id"]),
            "carrier_id": carrier_id,
            "route_id": route_id,
            "origin_warehouse_id": int(route["origin_warehouse_id"]),
            "destination_country": route["destination_country"],
            "destination_city": route["destination_city"],
            "planned_departure_ts": _iso(planned_departure),
            "actual_departure_ts": actual_departure_out,
            "planned_delivery_ts": _iso(planned_delivery),
            "actual_delivery_ts": actual_delivery_out,
            "shipment_status": status,
            "total_weight_kg": _round(row["total_weight_kg"], 3),
            "total_volume_m3": _round(row["total_volume_m3"], 4),
            "delay_minutes": delay_minutes,
            "created_at": _iso(planned_departure - timedelta(hours=2)),
        })
    return pd.DataFrame(rows)


def generate_tracking_events(rng: np.random.Generator, shipments: pd.DataFrame) -> pd.DataFrame:
    rows = []
    event_id = 1
    for _, s in shipments.iterrows():
        if s["shipment_status"] == "cancelled":
            event_types = ["created", "cancelled"]
        elif s["shipment_status"] == "in_transit":
            event_types = ["created", "picked_up", "departed_warehouse", "in_transit"]
        else:
            event_types = EVENT_TYPES_BASE
        planned_departure = datetime.fromisoformat(str(s["planned_departure_ts"]))
        planned_delivery = datetime.fromisoformat(str(s["planned_delivery_ts"]))
        total_seconds = max(3600, int((planned_delivery - planned_departure).total_seconds()))
        for pos, event_type in enumerate(event_types):
            ratio = pos / max(1, len(event_types) - 1)
            noise_minutes = int(rng.normal(0, 45))
            ts = planned_departure + timedelta(seconds=int(total_seconds * ratio), minutes=noise_minutes)
            payload = {
                "shipment_id": int(s["shipment_id"]),
                "status": str(event_type),
                "source_quality": _choice(rng, ["high", "medium", "medium", "low"]),
            }
            rows.append({
                "tracking_event_id": event_id,
                "shipment_id": int(s["shipment_id"]),
                "event_timestamp": _iso(ts),
                "event_type": event_type,
                "event_location": str(s["destination_city"]) if event_type in ["out_for_delivery", "delivered"] else f"Hub {int(rng.integers(1, 25)):02d}",
                "latitude": _round(rng.uniform(36.0, 53.0), 6),
                "longitude": _round(rng.uniform(-9.0, 15.0), 6),
                "event_source": _choice(rng, ["tms", "carrier_api", "mobile_app", "iot_gateway", "manual"]),
                "event_payload": json.dumps(payload, ensure_ascii=False),
                "created_at": _iso(ts + timedelta(minutes=int(rng.integers(1, 10)))),
            })
            event_id += 1
    return pd.DataFrame(rows)


def generate_incidents(rng: np.random.Generator, shipments: pd.DataFrame) -> pd.DataFrame:
    rows = []
    incident_id = 1
    for _, s in shipments.iterrows():
        base_prob = 0.07
        if int(s["delay_minutes"]) > 60:
            base_prob += 0.25
        if s["shipment_status"] == "cancelled":
            base_prob += 0.10
        if rng.random() >= base_prob:
            continue
        planned_departure = datetime.fromisoformat(str(s["planned_departure_ts"]))
        planned_delivery = datetime.fromisoformat(str(s["planned_delivery_ts"]))
        created_at = _random_dt(rng, planned_departure, max(planned_departure + timedelta(hours=1), planned_delivery))
        severity = _choice(rng, ["low", "medium", "medium", "high", "critical"])
        status = _choice(rng, ["open", "in_progress", "resolved", "resolved", "resolved"])
        resolved = ""
        if status == "resolved":
            resolved = _iso(created_at + timedelta(hours=int(rng.integers(2, 72))))
        incident_type = _choice(rng, INCIDENT_TYPES)
        rows.append({
            "incident_id": incident_id,
            "shipment_id": int(s["shipment_id"]),
            "incident_type": incident_type,
            "severity": severity,
            "created_at": _iso(created_at),
            "resolved_at": resolved,
            "incident_status": status,
            "description": f"{incident_type.replace('_', ' ').title()} detected for shipment {int(s['shipment_id'])}.",
        })
        incident_id += 1
    return pd.DataFrame(rows)


def generate_sensor_readings(rng: np.random.Generator, shipments: pd.DataFrame) -> pd.DataFrame:
    rows = []
    reading_id = 1
    sensor_types = ["temperature", "humidity", "vibration", "fuel_level", "door_open", "gps_speed"]
    units = {
        "temperature": "C",
        "humidity": "%",
        "vibration": "g",
        "fuel_level": "%",
        "door_open": "bool",
        "gps_speed": "kmh",
    }
    for _, s in shipments.iterrows():
        # Keep sample volume manageable: not every shipment has IoT readings.
        if rng.random() > 0.55:
            continue
        n_readings = int(rng.integers(1, 5))
        planned_departure = datetime.fromisoformat(str(s["planned_departure_ts"]))
        planned_delivery = datetime.fromisoformat(str(s["planned_delivery_ts"]))
        for _ in range(n_readings):
            sensor_type = _choice(rng, sensor_types)
            if sensor_type == "temperature":
                value = rng.normal(12, 8)
            elif sensor_type == "humidity":
                value = rng.uniform(25, 90)
            elif sensor_type == "vibration":
                value = abs(rng.normal(0.4, 0.25))
            elif sensor_type == "fuel_level":
                value = rng.uniform(5, 100)
            elif sensor_type == "door_open":
                value = 1 if rng.random() < 0.05 else 0
            else:
                value = rng.uniform(0, 110)
            rows.append({
                "sensor_reading_id": reading_id,
                "shipment_id": int(s["shipment_id"]),
                "warehouse_id": int(s["origin_warehouse_id"]),
                "route_id": int(s["route_id"]),
                "reading_ts": _iso(_random_dt(rng, planned_departure, max(planned_departure + timedelta(hours=1), planned_delivery))),
                "sensor_type": sensor_type,
                "sensor_value": _round(value, 4),
                "unit": units[sensor_type],
                "device_id": f"DEV-{int(rng.integers(1000, 9999))}",
                "created_at": _iso(planned_departure),
            })
            reading_id += 1
    return pd.DataFrame(rows)


def generate_documents(rng: np.random.Generator, orders: pd.DataFrame, shipments: pd.DataFrame, incidents: pd.DataFrame) -> pd.DataFrame:
    rows = []
    document_id = 1
    incident_by_shipment = incidents.groupby("shipment_id")["incident_id"].first().to_dict() if not incidents.empty else {}
    for _, s in shipments.iterrows():
        order_id = int(s["order_id"])
        shipment_id = int(s["shipment_id"])
        planned_departure = datetime.fromisoformat(str(s["planned_departure_ts"]))
        docs_for_shipment = ["delivery_note"]
        if s["shipment_status"] in ["delivered", "delayed"]:
            docs_for_shipment.append("proof_of_delivery")
        if rng.random() < 0.35:
            docs_for_shipment.append("invoice")
        if shipment_id in incident_by_shipment:
            docs_for_shipment.append("incident_email")
        for doc_type in docs_for_shipment:
            incident_id = int(incident_by_shipment[shipment_id]) if doc_type == "incident_email" and shipment_id in incident_by_shipment else ""
            fmt = _choice(rng, ["pdf", "pdf", "txt", "html", "docx"])
            rows.append({
                "document_id": document_id,
                "shipment_id": shipment_id,
                "order_id": order_id,
                "incident_id": incident_id,
                "document_type": doc_type,
                "document_date": _iso(planned_departure + timedelta(hours=int(rng.integers(1, 96)))),
                "storage_path": f"s3://logistics-book-lab/documents/{doc_type}/shipment_id={shipment_id}/{document_id}.{fmt}",
                "file_format": fmt,
                "language_code": _choice(rng, ["es", "en", "fr", "de", "it"]),
                "extracted_text": f"Synthetic {doc_type} for shipment {shipment_id}. Carrier, delivery status and operational notes are available for analysis.",
                "created_at": _iso(planned_departure),
            })
            document_id += 1
    return pd.DataFrame(rows)


def generate_emission_records(rng: np.random.Generator, shipments: pd.DataFrame, routes: pd.DataFrame, carriers: pd.DataFrame) -> pd.DataFrame:
    route_lookup = routes.set_index("route_id").to_dict("index")
    carrier_lookup = carriers.set_index("carrier_id").to_dict("index")
    rows = []
    for i, (_, s) in enumerate(shipments.iterrows(), start=1):
        route = route_lookup[int(s["route_id"])]
        carrier = carrier_lookup[int(s["carrier_id"])]
        fuel = _choice(rng, FUEL_BY_CARRIER_TYPE.get(carrier["carrier_type"], ["diesel"]))
        # Simplified synthetic factor for demo purposes only.
        factor = {
            "diesel": 0.095,
            "hybrid": 0.065,
            "electric": 0.025,
            "rail_mix": 0.035,
            "air_freight": 0.55,
            "sea_freight": 0.020,
        }[fuel]
        co2 = float(route["distance_km"]) * max(float(s["total_weight_kg"]), 1.0) * factor / 100.0
        planned_delivery = datetime.fromisoformat(str(s["planned_delivery_ts"]))
        rows.append({
            "emission_id": i,
            "shipment_id": int(s["shipment_id"]),
            "route_id": int(s["route_id"]),
            "co2_kg": _round(co2, 4),
            "fuel_type": fuel,
            "calculation_method": _choice(rng, ["distance_weight_factor", "carrier_factor", "estimated_telematics"]),
            "calculated_at": _iso(planned_delivery + timedelta(hours=2)),
            "created_at": _iso(planned_delivery + timedelta(hours=2, minutes=5)),
        })
    return pd.DataFrame(rows)


def generate_decision_log(rng: np.random.Generator, shipments: pd.DataFrame, incidents: pd.DataFrame) -> pd.DataFrame:
    rows = []
    decision_id = 1
    incident_by_shipment = incidents.groupby("shipment_id")["incident_id"].first().to_dict() if not incidents.empty else {}
    for _, s in shipments.iterrows():
        delay = int(s["delay_minutes"])
        should_decide = delay > 90 or int(s["shipment_id"]) in incident_by_shipment or rng.random() < 0.04
        if not should_decide:
            continue
        shipment_id = int(s["shipment_id"])
        planned_delivery = datetime.fromisoformat(str(s["planned_delivery_ts"]))
        if shipment_id in incident_by_shipment:
            dtype = "incident_escalation"
            action = "Escalate incident to operations supervisor and notify customer service."
        elif delay > 180:
            dtype = _choice(rng, ["route_change", "carrier_change", "customer_notification"])
            action = "Review route/carrier and notify customer about expected delay."
        else:
            dtype = "delay_risk"
            action = "Monitor shipment and prepare proactive notification if delay increases."
        status = _choice(rng, ["recommended", "accepted", "executed", "executed", "rejected"])
        rows.append({
            "decision_id": decision_id,
            "shipment_id": shipment_id,
            "incident_id": int(incident_by_shipment[shipment_id]) if shipment_id in incident_by_shipment else "",
            "decision_ts": _iso(planned_delivery - timedelta(hours=int(rng.integers(1, 12)))),
            "decision_type": dtype,
            "recommended_action": action,
            "decision_status": status,
            "decided_by": _choice(rng, ["human_operator", "ai_agent", "rules_engine", "human_operator"]),
            "confidence_score": _round(rng.uniform(0.55, 0.98), 4),
            "decision_reason": f"Synthetic decision generated from delay={delay} minutes and incident flag={shipment_id in incident_by_shipment}.",
            "action_taken": action if status in ["accepted", "executed"] else "No action taken.",
            "outcome": _choice(rng, ["delay_reduced", "customer_notified", "no_change", "incident_resolved", "pending_review"]),
            "created_at": _iso(planned_delivery),
        })
        decision_id += 1
    return pd.DataFrame(rows)


def generate_all(config: GenerationConfig) -> Dict[str, pd.DataFrame]:
    rng = _rng(config)
    customers = generate_customers(config, rng)
    partners = generate_partners(config, rng)
    warehouses = generate_warehouses(config, rng)
    carriers = generate_carriers(config, rng, partners)
    routes = generate_routes(config, rng, warehouses)
    orders, order_lines = generate_orders_and_lines(config, rng, customers)
    shipments = generate_shipments(config, rng, orders, order_lines, carriers, routes)
    tracking_events = generate_tracking_events(rng, shipments)
    incidents = generate_incidents(rng, shipments)
    sensor_readings = generate_sensor_readings(rng, shipments)
    documents = generate_documents(rng, orders, shipments, incidents)
    emission_records = generate_emission_records(rng, shipments, routes, carriers)
    decision_log = generate_decision_log(rng, shipments, incidents)

    tables = {
        "customers": customers,
        "partners": partners,
        "warehouses": warehouses,
        "carriers": carriers,
        "routes": routes,
        "orders": orders,
        "order_lines": order_lines,
        "shipments": shipments,
        "tracking_events": tracking_events,
        "incidents": incidents,
        "sensor_readings": sensor_readings,
        "documents": documents,
        "emission_records": emission_records,
        "decision_log": decision_log,
    }
    return tables


def write_tables(tables: Dict[str, pd.DataFrame], output_dir: Path, file_format: str = "csv") -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for table_name in TABLE_ORDER:
        df = tables[table_name]
        if file_format == "csv":
            df.to_csv(output_dir / f"{table_name}.csv", index=False)
        elif file_format == "parquet":
            df.to_parquet(output_dir / f"{table_name}.parquet", index=False)
        else:
            raise ValueError(f"Unsupported file_format={file_format}")
