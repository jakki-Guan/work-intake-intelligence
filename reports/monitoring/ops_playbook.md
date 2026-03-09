# Ops Playbook (MVP)

## Purpose

This playbook defines the first response steps when monitoring warnings appear in Work Intake Intelligence.

The MVP focuses on lightweight operational handling rather than full automation.

---

## 1. Warning Types

### A. Input Shift Warning
Examples:
- average input length increases materially
- channel mix changes
- language mix changes

Initial checks:
- inspect recent prediction logs
- confirm whether the traffic pattern changed intentionally
- compare recent requests with the frozen reference profile

Possible actions:
- continue monitoring if the change is expected
- retrain the routing model if performance degradation is also observed

---

### B. Confidence Warning
Examples:
- routing low-confidence rate rises
- average routing confidence drops

Initial checks:
- inspect recent routing predictions
- review whether new request wording differs from training data
- identify whether a specific request type or channel is driving the change

Possible actions:
- expand training data coverage
- test one upgrade path beyond TF-IDF + Logistic Regression
- temporarily route low-confidence cases to manual triage

---

### C. SLA Risk Rate Warning
Examples:
- predicted SLA at-risk rate rises materially

Initial checks:
- determine whether the shift is operationally plausible
- review whether the incoming workload is more incident-heavy or urgent
- confirm that feature inputs remain valid

Possible actions:
- monitor for persistence over multiple windows
- notify operations stakeholders if the trend is sustained
- review threshold choice if false positives appear too high

---

### D. Latency Warning
Examples:
- p95 latency exceeds threshold

Initial checks:
- confirm whether the service is running locally or under heavier load
- inspect recent request size changes
- verify logging and model loading behavior

Possible actions:
- optimize model loading / preprocessing
- reduce unnecessary per-request overhead
- scale deployment only if latency becomes operationally material

---

## 2. Retrain Guidance

Retraining should be considered when:
- warnings persist across multiple recent windows
- low confidence remains high
- business users report poor routing quality
- new request patterns are clearly different from the original baseline

MVP retrain approach:
1. collect a refreshed labeled sample
2. rerun baseline training
3. compare offline metrics and error analysis
4. update model version only if the new model improves the chosen trade-off

---

## 3. Rollback Guidance

Rollback should be considered when:
- a newly deployed model causes materially worse behavior
- confidence degrades sharply
- latency increases unexpectedly
- business-facing errors increase after a model update

MVP rollback approach:
1. restore the prior saved model artifact
2. verify `/health` and `/predict`
3. confirm monitoring metrics stabilize
4. document the rollback reason in the decision log

---

## 4. MVP Constraints

This project does not yet automate:
- notification delivery
- rollback execution
- production label feedback loops

These steps are documented manually first to keep the MVP simple and reproducible.