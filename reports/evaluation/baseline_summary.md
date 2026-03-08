# Baseline Evaluation Summary

## 1. Objective

This project includes two baseline modeling tasks:

1. **Routing prediction**
   - Predict the most likely work-intake queue based on ticket text.
2. **SLA risk prediction**
   - Predict whether a ticket is at risk of SLA breach using structured ticket attributes.

The goal of the baseline phase is not to maximize performance immediately, but to establish:
- a reproducible starting point
- interpretable model behavior
- clear error patterns
- a foundation for later API, monitoring, and reporting layers

---

## 2. Data Context

### 2.1 Routing Data Source
The routing task was migrated from a fully synthetic text setup to a public support-ticket dataset to improve text realism.

The public dataset provides fields such as:
- subject
- body
- queue
- priority
- type
- language

For the baseline version:
- only English records were kept
- fields were standardized into the project schema
- text input was constructed from `title + description`

### 2.2 SLA Risk Label
The public dataset does not contain a real historical SLA breach label.

Therefore, `sla_risk` in this project is a **proxy label**, derived from a reproducible business-style heuristic based on:
- priority
- routing queue
- channel
- requester type
- created hour

This means the SLA task should be interpreted as:
- a lightweight risk scoring workflow
- a reproducible analytics/AI baseline
- not a claim of production-grade historical truth

---

## 3. Routing Baseline

### 3.1 Task Definition
**Input:** ticket text (`title + description`)  
**Target:** `routing_queue`

### 3.2 Model
- TF-IDF vectorization
- Logistic Regression classifier

### 3.3 Baseline Iteration History

#### Initial synthetic-text routing baseline
The earliest routing baseline achieved unrealistically perfect performance because:
- class names or highly deterministic text patterns effectively leaked label identity
- the synthetic text was too templated
- train/test samples were too similar

This version was not treated as trustworthy for final evaluation.

#### Public-data routing baseline
After switching to public support-ticket text, performance became more realistic.

A standard TF-IDF + Logistic Regression baseline produced:
- accuracy around **0.46**

This was considered much more credible than the earlier synthetic result because the text became:
- more natural
- more varied
- less directly tied to queue names

### 3.4 Class Imbalance
Routing labels were strongly imbalanced.

Larger classes included:
- technical support
- product support
- customer service
- IT support

Smaller classes included:
- general inquiry
- human resources
- sales and pre-sales

This imbalance caused the initial public-data baseline to ignore some minority classes entirely.

### 3.5 Balanced Baseline Improvement
To address minority-class underprediction, Logistic Regression was updated with:

- `class_weight="balanced"`

This change:
- slightly reduced overall accuracy
- improved minority-class coverage
- made the baseline more operationally reasonable

### 3.6 Final Routing Baseline Interpretation
The balanced routing baseline is preferred over the unweighted version because it better reflects the needs of a real intake-routing workflow:
- not only strong performance on large queues
- but also non-zero recognition for smaller queues

### 3.7 Routing Takeaways
Key observations:
- routing on realistic public text is materially harder than routing on templated synthetic text
- class imbalance is a major factor
- the baseline is usable, interpretable, and clearly improvable
- next-step upgrades could include:
  - class-weight tuning
  - n-gram tuning
  - stronger text cleaning
  - a lightweight upgraded model such as LightGBM or transformer-based text classification

---

## 4. SLA Risk Baseline

### 4.1 Task Definition
**Input:** structured ticket fields  
**Target:** `sla_risk`

### 4.2 Features Used
The first SLA baseline used only structured attributes:
- channel
- priority
- requester_type
- routing_queue
- request_type
- created_hour

### 4.3 Model
- OneHotEncoder for categorical features
- StandardScaler for numeric feature(s)
- Logistic Regression classifier

### 4.4 Result
The structured SLA baseline achieved approximately:
- accuracy: **0.83**
- class 1 F1 score: **0.77**
- macro-average F1 around **0.82**

### 4.5 Why SLA Performed Better Than Routing
This result is meaningfully higher than routing performance, which is expected.

Reasons:
1. The SLA task is driven by structured business variables rather than noisier free text.
2. The SLA label is a proxy label derived from those same business-style factors.
3. The relationship between features and target is therefore more stable and more directly learnable.

This does **not** mean the SLA model is “better” in a universal sense.
It means:
- the task is structurally easier
- the label is more rule-aligned
- the baseline has higher signal density

### 4.6 SLA Label Audit
Before training the SLA model, the proxy label was audited through EDA.

The audit confirmed that higher risk was more common in expected scenarios such as:
- higher priority tickets
- support or outage-related queues
- off-hours creation times
- email-based intake

This made the proxy label sufficiently interpretable and reproducible for baseline modeling.

### 4.7 SLA Takeaways
Key observations:
- the SLA baseline is strong for a first structured model
- the result is reasonable given the proxy-label design
- the main limitation is that the target is not historical ground truth
- the baseline is still useful because it supports:
  - monitoring workflows
  - thresholding discussions
  - API integration
  - downstream operations reporting

---

## 5. Routing vs SLA: Comparison

| Dimension | Routing Baseline | SLA Baseline |
|---|---|---|
| Problem type | Multi-class classification | Binary classification |
| Input type | Free text | Structured fields |
| Data realism | Public support-ticket text | Public ticket metadata + derived proxy label |
| Difficulty | Higher | Lower |
| Main challenge | Class imbalance, semantic overlap | Proxy-label interpretation |
| Baseline model | TF-IDF + Logistic Regression | Structured Logistic Regression |
| Result pattern | Moderate performance, minority-class trade-off | Stronger and more stable performance |

### Key message
These two baselines play different roles:

- **Routing** demonstrates realistic NLP classification under noisy, imbalanced public ticket text.
- **SLA risk** demonstrates a lightweight, explainable risk-scoring workflow using structured operational features.

Together, they support the broader project goal of building a practical end-to-end work-intake intelligence pipeline.

---

## 6. Main Trade-offs Identified

### 6.1 Routing
- Higher overall accuracy can come at the cost of ignoring minority classes.
- Balanced class weighting reduces this failure mode, even if accuracy drops slightly.

### 6.2 SLA Risk
- Higher performance is easier to achieve because the label is derived from structured business rules.
- This improves reproducibility and explainability, but reduces historical realism.

### 6.3 Project-Level Trade-off
This project intentionally prioritizes:
- reproducibility
- explainability
- portfolio safety
- operational storytelling

over:
- raw benchmark chasing
- hidden proprietary realism
- overly complex modeling at the first baseline stage

---

## 7. Current Limitations

### Routing limitations
- strong class imbalance
- minority classes remain challenging
- text still contains overlap across support categories
- no upgraded text model yet

### SLA limitations
- label is a proxy, not a true SLA-breach outcome
- feature-label relationship is partly rule-driven
- no probability calibration or threshold analysis yet

### Shared limitations
- no production deployment evaluation yet
- no live drift monitoring evaluation yet
- no human-in-the-loop review process yet

---

## 8. Why These Baselines Are Still Valuable

Even with those limitations, the current baselines are valuable because they establish:

- an end-to-end modeling workflow
- reusable preprocessing logic
- saved model artifacts
- saved metrics artifacts
- realistic discussion points for trade-offs
- a strong foundation for:
  - FastAPI inference
  - monitoring dashboards
  - evaluation reports
  - future model upgrades

This is exactly what a strong flagship portfolio project needs at the baseline stage.

---

## 9. Next Steps

### Immediate next steps
1. package these results into a cleaner evaluation summary for README usage
2. expose model inference through the API layer
3. produce monitoring-ready prediction outputs
4. generate lightweight model comparison artifacts

### Likely modeling upgrades
- improved routing text model
- class imbalance strategies beyond simple weighting
- optional text-enhanced SLA model
- calibration / threshold analysis for SLA risk scores

---

## 10. Final Baseline Assessment

### Routing baseline
**Status:** acceptable, realistic, and improvable  
**Use in project:** retained as the main queue-routing baseline

### SLA baseline
**Status:** strong and interpretable for a proxy-label workflow  
**Use in project:** retained as the initial risk baseline

### Overall
The project now has two working baselines that are:
- reproducible
- explainable
- saved as model artifacts
- suitable for API and monitoring integration
- strong enough to support the next project phase