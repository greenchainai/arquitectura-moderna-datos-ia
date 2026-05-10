def get_user_context(user_id: str) -> dict:
    return {"user_id": user_id, "roles": ["operations"]}


def classify_intent(question: str) -> str:
    if "envío" in question.lower() or "shipment" in question.lower():
        return "shipment_status"
    return "unknown"


def extract_shipment_id(question: str) -> str:
    for token in question.replace(".", " ").split():
        if token.startswith("SHP-"):
            return token
    raise ValueError("Shipment id not found")


def call_tool(tool_name: str, input_payload: dict, user_context: dict) -> dict:
    if tool_name == "get_shipment_status":
        return {"shipment_id": input_payload["shipment_id"], "shipment_status": "DELAYED", "shipment_type": "EXPRESS", "destination_country": "ES", "delay_risk_score": 0.82, "open_incidents": 1}
    if tool_name == "search_logistics_policy":
        return {"policy_id": "POL-EXPRESS-DELAY", "summary": "Escalate if express delay risk is greater than 70%.", "source": "express_delay_policy_v2.md"}
    return {}


def generate_recommendation(question: str, shipment_status: dict, policy_context: dict) -> dict:
    if shipment_status.get("delay_risk_score", 0) > 0.70:
        return {"recommendation": "CREATE_ESCALATION_CASE", "severity": "HIGH", "requires_human_approval": True, "evidence": [shipment_status, policy_context]}
    return {"recommendation": "MONITOR", "requires_human_approval": False, "evidence": [shipment_status, policy_context]}


def log_agent_response(user_id: str, question: str, tools_used: list[str], response: dict) -> None:
    print({"user_id": user_id, "question": question, "tools_used": tools_used, "response": response})


def logistics_agent(user_id: str, question: str) -> dict:
    user_context = get_user_context(user_id)
    intent = classify_intent(question)
    if intent == "shipment_status":
        shipment_id = extract_shipment_id(question)
        status = call_tool("get_shipment_status", {"shipment_id": shipment_id}, user_context)
        policy = call_tool("search_logistics_policy", {"query": "procedimiento ante retraso de envío", "shipment_type": status.get("shipment_type"), "country": status.get("destination_country")}, user_context)
        recommendation = generate_recommendation(question, status, policy)
        log_agent_response(user_id, question, ["get_shipment_status", "search_logistics_policy"], recommendation)
        return recommendation
    return {"message": "No tengo suficiente contexto para resolver esta solicitud."}


if __name__ == "__main__":
    print(logistics_agent("user-001", "Revisa el envío SHP-10045 y dime si debo escalarlo."))
