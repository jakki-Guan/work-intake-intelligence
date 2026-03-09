# Demo Runbook

## Project one-liner

Work Intake Intelligence is a lightweight Applied AI / Analytics Engineering project for ticket routing, SLA risk prediction, and operational monitoring.

---

## Demo flow

### 1. Show the project README
Explain:
- the problem
- the two-model workflow
- why lightweight baselines were chosen first
- how monitoring and reporting were added

### 2. Show the API
Open:
- `/docs`
- `/health`
- `/predict`

Explain:
- routing prediction comes from ticket text
- SLA risk uses structured fields plus predicted routing queue

### 3. Run smoke test
Use:
- `scripts/smoke_test_api.ps1`

Explain:
- the system is reproducible
- the local API can be validated quickly

### 4. Show monitoring outputs
Highlight:
- prediction logging
- reference profile
- current-window vs baseline monitoring summary
- warning conditions in shifted demo workload

### 5. Show the Power BI dashboard
Highlight:
- total predictions
- SLA at-risk rate
- routing low-confidence rate
- latency
- current-window vs baseline checks

### 6. Close with next steps
Mention:
- better drift checks
- alert hooks
- top-k confidence monitoring
- retrain / rollback workflow refinement