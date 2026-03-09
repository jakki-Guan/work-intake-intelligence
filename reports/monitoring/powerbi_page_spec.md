# Power BI Monitoring Page Spec

## Page Goal
Show lightweight operational monitoring for Work Intake Intelligence.

## Data Sources
- `prediction_events.csv`
- `monitoring_checks.csv`

## Visuals

### 1. KPI Cards
- Predictions analyzed
- SLA at-risk rate
- Routing low-confidence rate
- p95 latency

### 2. Column Chart
- Count of predictions by routing label

### 3. Histogram or column chart
- Routing confidence distribution (binned)

### 4. Table
- Monitoring checks:
  - metric_name
  - current_value
  - reference_value
  - delta_ratio
  - status

### 5. Optional slicers
- channel
- sla_label
- routing_label

## Notes
Use sanitized synthetic data only.
Screenshots for portfolio should avoid local machine paths and personal identifiers.