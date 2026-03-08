"""
Train the baseline SLA risk model.
"""
from __future__ import annotations

import json
from datetime import datetime

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.utils.paths import RAW_DATA_DIR, MODELS_DIR, METRICS_DIR, ensure_project_dirs


def load_training_data() -> pd.DataFrame:
    input_path = RAW_DATA_DIR / "public_tickets_standardized_v1.csv"
    return pd.read_csv(input_path)


def build_pipeline() -> Pipeline:
    categorical_features = [
        "channel",
        "priority",
        "requester_type",
        "routing_queue",
        "request_type",
    ]

    numeric_features = [
        "created_hour",
    ]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numeric_features),
        ]
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("clf", LogisticRegression(max_iter=1000, random_state=42)),
        ]
    )

    return pipeline


def main() -> None:
    ensure_project_dirs()

    df = load_training_data()

    feature_cols = [
        "channel",
        "priority",
        "requester_type",
        "routing_queue",
        "request_type",
        "created_hour",
    ]
    target_col = "sla_risk"

    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    cm = confusion_matrix(y_test, y_pred).tolist()

    model_path = MODELS_DIR / "sla_baseline.joblib"
    metrics_path = METRICS_DIR / "sla_baseline_metrics.json"

    joblib.dump(pipeline, model_path)

    metrics_payload = {
        "model_name": "sla_baseline",
        "model_type": "structured_logistic_regression",
        "feature_columns": feature_cols,
        "target_column": target_col,
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "accuracy": accuracy,
        "generated_at": datetime.utcnow().isoformat(),
        "confusion_matrix": cm,
        "classification_report": report_dict,
    }

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    print(f"Saved model to: {model_path}")
    print(f"Saved metrics to: {metrics_path}")
    print(f"Train rows: {len(X_train)}")
    print(f"Test rows: {len(X_test)}")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nConfusion matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    main()