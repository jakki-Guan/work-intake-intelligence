"""
Train the baseline routing model.
"""
from __future__ import annotations

import json
from datetime import datetime

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.utils.paths import (
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    MODELS_DIR,
    METRICS_DIR,
    ensure_project_dirs,
)


def load_training_data() -> pd.DataFrame:
    input_path = PROCESSED_DATA_DIR / "work_intake_model_input_v2.csv"
    return pd.read_csv(input_path)


def build_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=1)),
            ("clf", LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced")),
        ]
    )


def main() -> None:
    ensure_project_dirs()

    df = load_training_data()

    X = df["text"]
    y = df["routing_queue"]

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
    report = classification_report(y_test, y_pred, output_dict=True)

    model_path = MODELS_DIR / "router_baseline.joblib"
    metrics_path = METRICS_DIR / "router_baseline_metrics.json"

    joblib.dump(pipeline, model_path)

    metrics_payload = {
        "model_name": "router_baseline",
        "model_type": "tfidf_logistic_regression",
        "class_weight": "balanced",
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "accuracy": accuracy,
        "generated_at": datetime.utcnow().isoformat(),
        "classification_report": report,
    }

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    print(f"Saved model to: {model_path}")
    print(f"Saved metrics to: {metrics_path}")
    print(f"Train rows: {len(X_train)}")
    print(f"Test rows: {len(X_test)}")
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))


if __name__ == "__main__":
    main()