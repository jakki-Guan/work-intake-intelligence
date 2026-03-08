"""
FastAPI application entry point.
"""

from __future__ import annotations

import logging
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI

from src.api.schemas import PredictRequest, PredictResponse
from src.api.service import predict_ticket
from src.monitoring.prediction_logger import build_prediction_event, append_event_jsonl

logger = logging.getLogger(__name__)

ROUTING_MODEL_VERSION = "routing_logreg_tfidf_balanced_v1"
SLA_MODEL_VERSION = "sla_logreg_structured_v1"
SLA_THRESHOLD = 0.5

app = FastAPI(
    title="Work Intake Intelligence API",
    version="0.1.0",
    description="Routing prediction + SLA risk prediction baseline API",
)


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "work-intake-intelligence-api",
    }


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    request_id = str(uuid4())
    start = perf_counter()

    result = predict_ticket(
        title=request.title,
        description=request.description,
        channel=request.channel,
        priority=request.priority,
        requester_type=request.requester_type,
        created_hour=request.created_hour,
        request_type=request.request_type,
    )

    latency_ms = (perf_counter() - start) * 1000

    combined_text = " ".join(
        part.strip()
        for part in [request.title or "", request.description or ""]
        if part and part.strip()
    )

    sla_label = "at_risk" if int(result["predicted_sla_risk"]) == 1 else "not_at_risk"

    try:
        event = build_prediction_event(
            request_id=request_id,
            text=combined_text,
            routing_label=result["predicted_routing_queue"],
            routing_confidence=float(result["routing_confidence"]),
            routing_top_3=[],
            sla_label=sla_label,
            sla_probability=float(result["sla_risk_probability"]),
            sla_threshold=SLA_THRESHOLD,
            latency_ms=latency_ms,
            model_versions={
                "routing": ROUTING_MODEL_VERSION,
                "sla": SLA_MODEL_VERSION,
            },
            channel=request.channel,
            language="en",
        )
        append_event_jsonl(event)
    except Exception:
        logger.exception("Prediction logging failed. request_id=%s", request_id)

    return PredictResponse(**result)