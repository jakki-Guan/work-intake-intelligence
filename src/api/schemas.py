"""
Pydantic schemas for API request and response objects.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    title: str = Field(..., description="Short ticket title")
    description: str = Field(..., description="Ticket description or body")
    channel: str = Field(..., description="Intake channel, e.g. email / portal / chat")
    priority: str = Field(..., description="Priority level, e.g. low / medium / high")
    requester_type: str = Field(..., description="Requester type, e.g. internal / external / vip")
    created_hour: int = Field(..., ge=0, le=23, description="Hour of day when the ticket was created")
    request_type: str = Field(..., description="Request type, e.g. request / problem")


class PredictResponse(BaseModel):
    input_text: str
    predicted_routing_queue: str
    routing_confidence: float
    predicted_sla_risk: int
    sla_risk_probability: float