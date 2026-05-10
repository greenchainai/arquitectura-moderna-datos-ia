"""
Scoring predictivo simple para arquitectura. No es un modelo ML productivo.
"""
import pandas as pd


def score_delay_risk(row: pd.Series) -> float:
    score = 0.10
    score += min(row.get("historical_delay_rate", 0), 1.0) * 0.45
    score += min(row.get("incident_count", 0), 5) * 0.08
    score += 0.15 if row.get("carrier_service_level") == "ECONOMY" else 0
    score += 0.10 if row.get("route_type") == "INTERNATIONAL" else 0
    return round(min(score, 0.99), 4)


def add_delay_score(features: pd.DataFrame) -> pd.DataFrame:
    features = features.copy()
    features["delay_risk_score"] = features.apply(score_delay_risk, axis=1)
    return features


if __name__ == "__main__":
    df = pd.DataFrame([{"shipment_id": "SHP-10045", "historical_delay_rate": 0.35, "incident_count": 1, "carrier_service_level": "ECONOMY", "route_type": "INTERNATIONAL"}])
    print(add_delay_score(df))
