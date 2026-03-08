from __future__ import annotations

import joblib
import pandas as pd

from src.utils.paths import MODELS_DIR


ROUTER_MODEL_PATH = MODELS_DIR / "router_baseline.joblib"
SLA_MODEL_PATH = MODELS_DIR / "sla_baseline.joblib"


def build_text(title: str, description: str) -> str:
    title = str(title).strip().lower()
    description = str(description).strip().lower()
    text = f"{title} {description}"
    text = " ".join(text.split())
    return text


def load_models():
    if not ROUTER_MODEL_PATH.exists():
        raise FileNotFoundError(f"Router model not found: {ROUTER_MODEL_PATH}")

    if not SLA_MODEL_PATH.exists():
        raise FileNotFoundError(f"SLA model not found: {SLA_MODEL_PATH}")

    router_model = joblib.load(ROUTER_MODEL_PATH)
    sla_model = joblib.load(SLA_MODEL_PATH)
    return router_model, sla_model


router_model, sla_model = load_models()


def predict_ticket(
    title: str,
    description: str,
    channel: str,
    priority: str,
    requester_type: str,
    created_hour: int,
    request_type: str,
) -> dict:
    # 1) Build text input for routing
    input_text = build_text(title=title, description=description)

    # 2) Predict routing queue
    routing_pred = router_model.predict([input_text])[0]

    routing_proba = None
    if hasattr(router_model, "predict_proba"):
        routing_classes = list(router_model.classes_)
        routing_probs = router_model.predict_proba([input_text])[0]
        routing_index = routing_classes.index(routing_pred)
        routing_proba = float(routing_probs[routing_index])
    else:
        routing_proba = 0.0

    # 3) Build structured input for SLA prediction
    sla_input = pd.DataFrame(
        [
            {
                "channel": channel,
                "priority": priority,
                "requester_type": requester_type,
                "routing_queue": routing_pred,
                "request_type": request_type,
                "created_hour": created_hour,
            }
        ]
    )

    # 4) Predict SLA risk
    sla_pred = int(sla_model.predict(sla_input)[0])

    sla_proba = 0.0
    if hasattr(sla_model, "predict_proba"):
        sla_probs = sla_model.predict_proba(sla_input)[0]
        # class 1 probability
        sla_proba = float(sla_probs[1])

    return {
        "input_text": input_text,
        "predicted_routing_queue": routing_pred,
        "routing_confidence": routing_proba,
        "predicted_sla_risk": sla_pred,
        "sla_risk_probability": sla_proba,
    }