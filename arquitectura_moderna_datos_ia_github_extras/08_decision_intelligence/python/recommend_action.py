def recommend_action(
    delay_risk_score: float,
    customer_segment: str,
    open_incidents: int,
    co2_impact_score: float
) -> str:
    if delay_risk_score >= 0.85 and customer_segment == "STRATEGIC":
        return "ESCALATE_CRITICAL"

    if delay_risk_score >= 0.75 and open_incidents > 0:
        return "ESCALATE_HIGH"

    if delay_risk_score >= 0.65:
        return "REVIEW_BY_OPERATOR"

    if co2_impact_score > 0.80:
        return "REVIEW_SUSTAINABILITY_OPTION"

    return "MONITOR"


if __name__ == "__main__":
    print(recommend_action(0.82, "STRATEGIC", 1, 0.35))
