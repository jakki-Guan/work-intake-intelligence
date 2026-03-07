# DECISIONS

## D-001: Project Scope
This flagship project will focus on:
- intelligent work-item routing
- SLA risk prediction
- operations monitoring

The initial version will not include:
- RAG
- agent workflows
- recommendation systems
- automated case resolution

## D-002: Data Strategy
This project will use synthetic data only.

No real company data, real employee names, internal URLs, or sensitive organizational details will be used.

## D-003: Local Development Stack
Default local setup:
- Windows
- Python 3.11
- venv
- VS Code

## D-004: Database Choice
DuckDB is the default local analytical store for this project.

Postgres is not part of the initial version unless later requirements clearly justify the change.

## D-005: Baseline Modeling Strategy
Baseline-first approach:
- Routing model: TF-IDF + Logistic Regression
- SLA risk model: structured features + Logistic Regression

Only one upgrade level will be considered later, most likely LightGBM.

## D-006: Monitoring Strategy
Monitoring will stay lightweight and practical in the initial version, including:
- input length distribution
- class mix distribution
- confidence distribution
- threshold-based alerts

## D-007: Deployment Strategy
Local MVP first.

Cloud deployment is optional and will only be considered after the local end-to-end workflow is complete.