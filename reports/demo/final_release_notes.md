# Final Release Notes

## Work Intake Intelligence - MVP Release

This release includes an end-to-end Applied AI / Analytics Engineering workflow for:

- ticket routing prediction
- SLA risk prediction
- API serving
- prediction logging
- lightweight monitoring
- Power BI operations reporting

### Included in this release
- standardized support-ticket data preparation
- TF-IDF + Logistic Regression routing baseline
- structured Logistic Regression SLA baseline
- FastAPI `/health` and `/predict` endpoints
- structured prediction logging
- reference-profile vs current-window monitoring summary
- monitoring documentation and ops playbook
- Power BI monitoring dashboard screenshot and CSV exports

### Key project themes
- reproducibility
- lightweight deployment
- practical monitoring
- interview-ready system design

## Detailed Architecture

```mermaid
flowchart TD
    subgraph DATA["Data Preparation"]
        A["Public support-ticket dataset<br/>raw text + raw metadata"]
        B["src/data/prepare_public_ticket_data.py<br/>standardize schema + derive fields"]
        C[("data/raw/public_tickets_standardized_v1.csv")]
        A --> B --> C
    end

    subgraph TRAIN["Model Training"]
        D["src/models/train_router_baseline.py<br/>TF-IDF + Logistic Regression"]
        E["src/models/train_sla_baseline.py<br/>structured Logistic Regression"]
        F[("artifacts/models/router_baseline.joblib")]
        G[("artifacts/models/sla_baseline.joblib")]
        H[("artifacts/metrics/*.json")]

        C --> D --> F
        C --> E --> G
        D --> H
        E --> H
    end

    subgraph SERVE["Inference API"]
        I["Client / Ops user"]
        J["src/api/main.py<br/>FastAPI `/health` + `/predict`"]
        K["src/api/service.py<br/>build text + load models"]
        L["Routing prediction<br/>queue + confidence"]
        M["SLA prediction<br/>uses structured fields + predicted queue"]
        N["API response"]

        I --> J --> K
        F --> K --> L
        L --> M
        G --> M --> N
    end

    subgraph OBS["Monitoring & Reporting"]
        O["src/monitoring/prediction_logger.py<br/>structured JSONL event"]
        P[("data/monitoring/prediction_logs")]
        Q["src/monitoring/reference_profile.py<br/>saved baseline profile"]
        R["src/monitoring/run_monitoring.py<br/>current vs reference checks"]
        S[("reports/monitoring/generated")]
        T["src/monitoring/export_monitoring_csv.py"]
        U[("data/monitoring/powerbi/*.csv")]
        V["Power BI monitoring dashboard"]

        N --> O --> P
        P --> Q
        P --> R
        Q --> R --> S
        P --> T
        S --> T --> U --> V
    end

    classDef data fill:#E8F3FF,stroke:#2B6CB0,color:#12324A,stroke-width:1.5px;
    classDef train fill:#EAF7EE,stroke:#2F855A,color:#143825,stroke-width:1.5px;
    classDef serve fill:#FFF4DB,stroke:#B7791F,color:#4A2F0B,stroke-width:1.5px;
    classDef obs fill:#FDEBEC,stroke:#C05668,color:#4A1F28,stroke-width:1.5px;
    classDef store fill:#F4F5F7,stroke:#4A5568,color:#1A202C,stroke-width:1.5px;

    class A,B data;
    class D,E train;
    class I,J,K,L,M,N serve;
    class O,Q,R,T,V obs;
    class C,F,G,H,P,S,U store;
```

### Diagram legend
- Blue: data preparation
- Green: model training
- Gold: inference serving
- Rose: monitoring and reporting
- Gray: stored datasets, models, metrics, and exports
