# Work Intake Intelligence
 
## Overview
Work Intake Intelligence is a lightweight Applied AI / Analytics Engineering portfolio project focused on:
 
- intelligent work-item routing
- SLA risk prediction
- operations monitoring
 
The goal is to build a project that is:
 
- reproducible
- evaluable
- deployable
- monitorable
- interview-ready
 
---
 
## Problem
Operations teams often receive incoming tickets, requests, or work items from multiple channels. Manual triage can be slow and inconsistent, and SLA risk is often identified too late.
 
This project simulates a practical analytics/AI workflow that helps:
 
- predict the most likely routing queue
- flag tickets that are likely at risk of SLA breach
- expose predictions through an API
- support monitoring and reporting layers
 
---
 
## Proposed Solution
This project builds a lightweight end-to-end workflow that:
 
1. predicts the likely routing queue for an incoming work item
2. predicts whether the work item is at risk of SLA breach
3. exposes a FastAPI `/predict` endpoint
4. supports lightweight monitoring for drift and score distribution changes
5. prepares outputs for an operations dashboard
 
---
 
## Data
The project started with synthetic data exploration, but the current baseline workflow uses a **public support-ticket dataset** as the primary text source.
 
### Current data approach
- public support-ticket text improves realism for routing classification
- English-only subset used for the baseline version
- raw public fields are standardized into a unified project schema
- additional structured fields such as `channel`, `requester_type`, and `created_hour` are programmatically derived
- `sla_risk` is a **reproducible proxy label**, not a historical ground-truth breach label
 
### Key standardized fields
- `ticket_id`
- `title`
- `description`
- `channel`
- `priority`
- `requester_type`
- `created_hour`
- `routing_queue`
- `request_type`
- `language`
- `sla_risk`
 
---
 
## Initial Technical Direction
- Python 3.11
- venv
- scikit-learn baseline models
- FastAPI
- public support-ticket dataset + standardized schema
- lightweight monitoring design
- Power BI-ready reporting outputs
 
---
 
## Baseline Strategy
 
### Routing model
- input: `title + description`
- baseline: TF-IDF + Logistic Regression
- improvement: `class_weight="balanced"` to better handle minority queues
 
### SLA risk model
- input: structured ticket attributes
- baseline: Logistic Regression with encoded categorical features
- target: proxy `sla_risk` label derived from business-style heuristics
 
---
 
## Current Results
 
### Routing baseline
The routing task became much more realistic after moving from templated synthetic text to public support-ticket text.
 
Current routing baseline characteristics:
- public ticket text classification
- clear class imbalance across queues
- balanced Logistic Regression retained as the preferred baseline
- moderate overall performance, with improved minority-class recognition after balancing
 
### SLA baseline
The SLA baseline uses structured fields:
- `channel`
- `priority`
- `requester_type`
- `routing_queue`
- `request_type`
- `created_hour`
 
Current SLA baseline achieved:
- accuracy around **0.83**
- balanced performance across both classes
- a reproducible and interpretable proxy-risk workflow
 
### Key interpretation
- routing is harder because it depends on noisier free text and imbalanced multi-class labels
- SLA risk is easier because it uses structured features and a rule-aligned proxy label
 
More detailed discussion is documented in:
 
`reports/evaluation/baseline_summary.md`
 
---
 
## Inference API
 
A lightweight FastAPI service is included to demonstrate end-to-end inference.
 
### Endpoints
 
#### `GET /health`
Returns a simple health check response for service validation.
 
#### `POST /predict`
Runs a two-step inference flow:
 
1. predict the most likely `routing_queue` from ticket text
2. use the predicted queue together with structured inputs to predict `sla_risk`
 
### Example Request
 
```json
{
  "title": "VPN connection keeps dropping",
  "description": "User reports unstable remote access since this morning and needs help urgently.",
  "channel": "email",
  "priority": "high",
  "requester_type": "external",
  "created_hour": 7,
  "request_type": "problem"
}
```
 
### Example Response
 
```json
{
  "input_text": "vpn connection keeps dropping user reports unstable remote access since this morning and needs help urgently.",
  "predicted_routing_queue": "it support",
  "routing_confidence": 0.1649,
  "predicted_sla_risk": 1,
  "sla_risk_probability": 0.9871
}
```
 
### Run Locally
 
```bash
python -m uvicorn src.api.main:app --reload
```
 
Then open:
- `http://127.0.0.1:8000/health`
- `http://127.0.0.1:8000/docs`
 
---
 
## Current Status
Completed so far:
 
- local project initialization
- Git repository setup
- virtual environment setup
- dependency installation
- project directory skeleton
- public ticket data standardization
- routing baseline training
- balanced routing baseline improvement
- SLA baseline training
- baseline evaluation summary
- FastAPI `/predict` inference endpoint
 
---
 
## Next Steps
Planned next steps:
 
- add prediction logging for monitoring-ready outputs
- define lightweight drift and score-distribution checks
- prepare monitoring report artifacts
- add API usage notes and sanitized demo screenshots
- prepare dashboard-ready reporting outputs
- optionally upgrade routing modeling beyond the first baseline
