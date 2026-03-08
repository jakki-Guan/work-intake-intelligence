# src/monitoring/schemas.py
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RoutingPrediction(BaseModel):
    label: str
    confidence: float
    top_3: List[Dict[str, float]] = Field(default_factory=list)


class SlaPrediction(BaseModel):
    label: str
    probability: float
    threshold: float


class InputProfile(BaseModel):
    channel: Optional[str] = None
    language: Optional[str] = None
    text_hash: str
    text_length_chars: int
    text_length_words: int


class PredictionLogEvent(BaseModel):
    event_version: str = "1.0"
    event_type: str = "prediction"
    event_ts: str
    request_id: str

    model_versions: Dict[str, str]
    input_profile: InputProfile

    routing_prediction: RoutingPrediction
    sla_prediction: SlaPrediction

    latency_ms: float
    status: str = "success"


class MonitoringCheck(BaseModel):
    metric_name: str
    current_value: float
    reference_value: float
    threshold: float
    status: str  # pass / warn / fail


class MonitoringSummary(BaseModel):
    summary_version: str = "1.0"
    generated_at: str
    window_start: str
    window_end: str
    n_predictions: int
    checks: List[MonitoringCheck] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)