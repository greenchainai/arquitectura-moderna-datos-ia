import hashlib
import json
from datetime import datetime
from pathlib import Path
import requests

API_URL = "https://api.example.com/tracking/events"
OUTPUT_DIR = Path("data/landing/tracking")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def calculate_hash(record: dict) -> str:
    raw = json.dumps(record, sort_keys=True)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def fetch_tracking_events(since_timestamp: str) -> list[dict]:
    response = requests.get(API_URL, params={"since": since_timestamp}, timeout=30)
    response.raise_for_status()
    return response.json()["events"]


def write_landing_file(events: list[dict]) -> str:
    batch_id = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    output_file = OUTPUT_DIR / f"tracking_events_{batch_id}.jsonl"
    with output_file.open("w", encoding="utf-8") as file:
        for event in events:
            envelope = {
                "source_system": "tracking_api",
                "ingestion_batch_id": batch_id,
                "ingestion_timestamp": datetime.utcnow().isoformat(),
                "payload_hash": calculate_hash(event),
                "payload": event,
            }
            file.write(json.dumps(envelope, ensure_ascii=False) + "\n")
    return str(output_file)


if __name__ == "__main__":
    events = fetch_tracking_events("2026-04-01T00:00:00")
    print(write_landing_file(events))
