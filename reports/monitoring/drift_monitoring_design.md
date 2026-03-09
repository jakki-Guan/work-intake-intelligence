# Drift and Confidence Monitoring Design

## Goal

The production system does not assume immediate ground-truth labels.
Therefore, the first monitoring layer focuses on:
- input distribution shift
- output distribution shift
- confidence movement
- operational latency

This is a practical MVP for internal ticket-routing workflows.

---

## 1. Monitoring Layers

### A. Input Monitoring
Track changes in request characteristics:
- text length (chars / words)
- channel mix
- language mix

### B. Prediction Monitoring
Track changes in model outputs:
- routing class mix
- routing confidence
- SLA risk probability
- SLA at-risk rate

### C. Operational Monitoring
Track service health:
- request volume
- latency
- logging failures
- schema compatibility

---

## 2. Initial MVP Checks

The MVP batch monitor currently checks:
- average input text length
- SLA at-risk rate
- routing low-confidence rate
- p95 latency

These checks are lightweight and interpretable.

---

## 3. Reference Baseline

The initial reference profile is generated from a saved set of historical prediction logs.

Later upgrades may use:
- holdout validation output
- rolling 30-day production baseline
- segment-level baselines by channel

---

## 4. Suggested Future Drift Checks

### Input Drift
- text_length_mean_delta_pct
- channel_mix_psi
- language_mix_psi

### Output Drift
- routing_class_mix_psi
- sla_positive_rate_delta
- mean_confidence_delta

### Confidence Monitoring
- routing_low_confidence_rate
- average routing confidence
- average SLA risk probability

### Operational Monitoring
- p95 latency
- error rate
- logging failure count

---

## 5. Initial Threshold Ideas

- text length mean delta > 20% -> warn
- routing class mix PSI > 0.20 -> warn
- routing class mix PSI > 0.30 -> fail
- SLA at-risk rate delta > 10% -> warn
- routing low-confidence rate > 25% -> warn
- p95 latency > 500 ms -> warn

Thresholds should be tuned after collecting more stable usage data.

---

## 6. Ops Playbook Direction

If warnings persist:
1. inspect prediction logs
2. compare recent inputs against reference profile
3. review confidence degradation
4. confirm whether drift is data-related or operational
5. retrain or rollback if business impact is material