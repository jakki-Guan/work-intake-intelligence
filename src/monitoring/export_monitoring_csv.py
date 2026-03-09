from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from src.monitoring.reference_profile import load_prediction_logs


def flatten_prediction_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "event_ts": row.get("event_ts"),
        "request_id": row.get("request_id"),
        "routing_model_version": row.get("model_versions", {}).get("routing"),
        "sla_model_version": row.get("model_versions", {}).get("sla"),
        "channel": row.get("input_profile", {}).get("channel"),
        "language": row.get("input_profile", {}).get("language"),
        "text_length_chars": row.get("input_profile", {}).get("text_length_chars"),
        "text_length_words": row.get("input_profile", {}).get("text_length_words"),
        "routing_label": row.get("routing_prediction", {}).get("label"),
        "routing_confidence": row.get("routing_prediction", {}).get("confidence"),
        "sla_label": row.get("sla_prediction", {}).get("label"),
        "sla_probability": row.get("sla_prediction", {}).get("probability"),
        "sla_threshold": row.get("sla_prediction", {}).get("threshold"),
        "latency_ms": row.get("latency_ms"),
        "status": row.get("status"),
    }


def export_prediction_events_csv(
    log_dir: str = "data/monitoring/prediction_logs",
    output_path: str = "data/monitoring/powerbi/prediction_events.csv",
    limit: int | None = None,
) -> str:
    rows = load_prediction_logs(log_dir=log_dir, limit=limit)
    flat_rows = [flatten_prediction_row(row) for row in rows]

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    if not flat_rows:
        out.write_text("", encoding="utf-8")
        return str(out)

    fieldnames = list(flat_rows[0].keys())
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_rows)

    return str(out)


def load_monitoring_summary(
    path: str = "reports/monitoring/generated/monitoring_summary.json",
) -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        return {}
    return json.loads(file_path.read_text(encoding="utf-8"))


def export_monitoring_checks_csv(
    summary_path: str = "reports/monitoring/generated/monitoring_summary.json",
    output_path: str = "data/monitoring/powerbi/monitoring_checks.csv",
) -> str:
    summary = load_monitoring_summary(summary_path)
    checks = summary.get("checks", {})

    rows: list[dict[str, Any]] = []
    for metric_name, detail in checks.items():
        rows.append(
            {
                "generated_at": summary.get("generated_at"),
                "n_predictions": summary.get("n_predictions"),
                "metric_name": metric_name,
                "current_value": detail.get("current_value"),
                "reference_value": detail.get("reference_value"),
                "delta_ratio": detail.get("delta_ratio"),
                "status": detail.get("status"),
            }
        )

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        out.write_text("", encoding="utf-8")
        return str(out)

    fieldnames = list(rows[0].keys())
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return str(out)


if __name__ == "__main__":
    events_path = export_prediction_events_csv(limit=50)
    checks_path = export_monitoring_checks_csv()

    print(f"Saved prediction events CSV to: {events_path}")
    print(f"Saved monitoring checks CSV to: {checks_path}")