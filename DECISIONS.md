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

## D-008: Routing Baseline Selection
For routing, the `class_weight="balanced"` Logistic Regression version is kept as the main baseline candidate.

Reason:
- the routing labels are not perfectly balanced
- this version is more reasonable for queue prediction under class imbalance
- it improves the baseline without adding much system complexity

The non-balanced version is still useful as a comparison point in evaluation.

## D-009: API Surface
The initial API surface includes:
- `/health`
- `/predict`

The MVP will return both:
- routing prediction
- SLA risk prediction

Separate task-specific endpoints are deferred unless later usability or deployment needs justify the split.

## D-010: Prediction Logging Storage
Prediction logging uses local append-only JSONL files in the MVP.

Reason:
- easy to implement
- easy to inspect locally
- good enough for reproducible monitoring demos

A later upgrade may move logs to DuckDB or Parquet if more robust querying is needed.

## D-011: Monitoring Privacy Rule
Operational prediction logs will not store raw ticket text.

Instead, logs store only:
- text hash
- text length metadata
- channel / language metadata
- prediction outputs
- latency
- model version

This keeps the project safer for portfolio use and aligned with privacy-conscious design.

## D-012: Monitoring Execution Mode
Monitoring will start as a lightweight batch process rather than real-time streaming.

Initial monitoring outputs will focus on:
- average input length
- SLA at-risk rate
- routing low-confidence rate
- p95 latency

Real-time alert delivery is deferred until the batch monitoring workflow is complete and stable.

## D-013: Monitoring Window Strategy
Batch monitoring compares a frozen reference profile against a recent prediction window rather than the full accumulated log history.

Reason:
- more realistic for operational monitoring
- easier to interpret than comparing against all historical logs
- helps recent shifts surface more clearly in summary outputs