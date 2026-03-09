# Monitoring Output Schema

## 1. Purpose

This project uses lightweight structured monitoring outputs to support:
- inference traceability
- confidence monitoring
- input/output distribution checks
- future drift alerting

The MVP separates:
1. event-level prediction logs
2. batch-level monitoring summaries

---

## 2. Prediction Log Event

One structured event is written for each `/predict` API call.

### Key fields

- `event_version`: schema version for log compatibility
- `event_type`: currently fixed as `prediction`
- `event_ts`: UTC timestamp when the inference event is logged
- `request_id`: unique request identifier
- `model_versions`: model version map for routing and SLA models

### Input profile fields

- `channel`: request channel
- `language`: inferred or default language
- `text_hash`: SHA256 hash of the combined input text
- `text_length_chars`: combined input text length in characters
- `text_length_words`: combined input text length in words

### Routing prediction fields

- `label`: predicted routing queue
- `confidence`: top predicted class confidence
- `top_3`: optional top-3 class list for future use

### SLA prediction fields

- `label`: `at_risk` or `not_at_risk`
- `probability`: probability of SLA risk
- `threshold`: operational classification threshold

### Operational fields

- `latency_ms`: end-to-end inference latency
- `status`: request processing status

### Privacy note

Raw ticket text is not stored in monitoring logs.
Only hashed and length-based input metadata is retained.

---

## 3. Monitoring Summary

A monitoring summary is generated in batch over a selected time window.

### Key fields

- `generated_at`
- `window_start`
- `window_end`
- `n_predictions`
- `checks`
- `notes`

### Initial checks in MVP

- average input length
- SLA at-risk rate
- routing low-confidence rate
- p95 latency

---

## 4. Example Prediction Log

```json
{
  "event_version": "1.0",
  "event_type": "prediction",
  "event_ts": "2026-03-08T16:18:14.156680+00:00",
  "request_id": "d1e90334-f5f2-47ec-b8f6-12e5cdd93135",
  "model_versions": {
    "routing": "routing_logreg_tfidf_balanced_v1",
    "sla": "sla_logreg_structured_v1"
  },
  "input_profile": {
    "channel": "email",
    "language": "en",
    "text_hash": "9553b47f5d17406a414c18283d174e83b5282bff493acf9edd73272171355be4",
    "text_length_chars": 109,
    "text_length_words": 16
  },
  "routing_prediction": {
    "label": "it support",
    "confidence": 0.164893,
    "top_3": []
  },
  "sla_prediction": {
    "label": "at_risk",
    "probability": 0.987088,
    "threshold": 0.5
  },
  "latency_ms": 14.64,
  "status": "success"
}