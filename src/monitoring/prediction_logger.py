# src/monitoring/prediction_logger.py
import hashlib
import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Any, Dict, Optional

from src.monitoring.schemas import (
    InputProfile,
    PredictionLogEvent,
    RoutingPrediction,
    SlaPrediction,
)


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def build_prediction_event(
    *,
    request_id: str,
    text: str,
    routing_label: str,
    routing_confidence: float,
    routing_top_3: list[dict[str, float]],
    sla_label: str,
    sla_probability: float,
    sla_threshold: float,
    latency_ms: float,
    model_versions: Dict[str, str],
    channel: Optional[str] = None,
    language: Optional[str] = "en",
) -> PredictionLogEvent:
    words = text.split()

    return PredictionLogEvent(
        event_ts=datetime.now(UTC).isoformat(),
        request_id=request_id,
        model_versions=model_versions,
        input_profile=InputProfile(
            channel=channel,
            language=language,
            text_hash=hash_text(text),
            text_length_chars=len(text),
            text_length_words=len(words),
        ),
        routing_prediction=RoutingPrediction(
            label=routing_label,
            confidence=round(routing_confidence, 6),
            top_3=routing_top_3,
        ),
        sla_prediction=SlaPrediction(
            label=sla_label,
            probability=round(sla_probability, 6),
            threshold=sla_threshold,
        ),
        latency_ms=round(latency_ms, 2),
        status="success",
    )


def append_event_jsonl(event: PredictionLogEvent, output_dir: str = "data/monitoring/prediction_logs") -> str:
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"predictions_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    out_path = out_dir / file_name

    with out_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event.model_dump(), ensure_ascii=False) + "\n")

    return str(out_path)