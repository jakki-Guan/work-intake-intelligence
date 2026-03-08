from __future__ import annotations

import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Any

from src.monitoring.reference_profile import build_reference_profile, load_prediction_logs


def load_reference_profile(path: str = "data/monitoring/reference/reference_profile.json") -> dict[str, Any]:
    file_path = Path(path)
    if not file_path.exists():
        return {}
    return json.loads(file_path.read_text(encoding="utf-8"))


def compare_metric(current: float, reference: float, warn_ratio: float = 0.2) -> dict[str, Any]:
    if reference == 0:
        delta_ratio = 0.0 if current == 0 else 1.0
    else:
        delta_ratio = abs(current - reference) / abs(reference)

    status = "pass"
    if delta_ratio > warn_ratio:
        status = "warn"

    return {
        "current_value": round(current, 4),
        "reference_value": round(reference, 4),
        "delta_ratio": round(delta_ratio, 4),
        "status": status,
    }


def build_monitoring_summary(
    current_profile: dict[str, Any],
    reference_profile: dict[str, Any],
) -> dict[str, Any]:
    now = datetime.now(UTC).isoformat()

    checks = {
        "avg_text_length_chars": compare_metric(
            current_profile.get("avg_text_length_chars", 0.0),
            reference_profile.get("avg_text_length_chars", 0.0),
            warn_ratio=0.2,
        ),
        "sla_at_risk_rate": compare_metric(
            current_profile.get("sla_at_risk_rate", 0.0),
            reference_profile.get("sla_at_risk_rate", 0.0),
            warn_ratio=0.2,
        ),
        "routing_low_confidence_rate": compare_metric(
            current_profile.get("routing_low_confidence_rate", 0.0),
            reference_profile.get("routing_low_confidence_rate", 0.0),
            warn_ratio=0.2,
        ),
        "p95_latency_ms": compare_metric(
            current_profile.get("p95_latency_ms", 0.0),
            reference_profile.get("p95_latency_ms", 0.0),
            warn_ratio=0.5,
        ),
    }

    return {
        "summary_version": "1.0",
        "generated_at": now,
        "n_predictions": current_profile.get("n_predictions", 0),
        "current_profile": current_profile,
        "reference_profile": reference_profile,
        "checks": checks,
        "notes": [
            "MVP monitoring uses lightweight batch comparison against a saved reference profile.",
            "This version focuses on input length, confidence movement, SLA risk rate, and latency.",
        ],
    }


def save_json(summary: dict[str, Any], path: str = "reports/monitoring/generated/monitoring_summary.json") -> str:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return str(out)


def save_markdown(summary: dict[str, Any], path: str = "reports/monitoring/generated/monitoring_summary.md") -> str:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Monitoring Summary",
        "",
        f"- Generated at: {summary['generated_at']}",
        f"- Predictions analyzed: {summary['n_predictions']}",
        "",
        "## Current Profile",
        "",
    ]

    for k, v in summary["current_profile"].items():
        lines.append(f"- {k}: {v}")

    lines.extend(["", "## Checks", ""])

    for metric_name, detail in summary["checks"].items():
        lines.append(f"### {metric_name}")
        lines.append(f"- current_value: {detail['current_value']}")
        lines.append(f"- reference_value: {detail['reference_value']}")
        lines.append(f"- delta_ratio: {detail['delta_ratio']}")
        lines.append(f"- status: {detail['status']}")
        lines.append("")

    lines.extend(["## Notes", ""])
    for note in summary["notes"]:
        lines.append(f"- {note}")

    out.write_text("\n".join(lines), encoding="utf-8")
    return str(out)

if __name__ == "__main__":
    rows = load_prediction_logs(limit=10)
    current_profile = build_reference_profile(rows)
    reference_profile = load_reference_profile()
    summary = build_monitoring_summary(current_profile, reference_profile)

    json_path = save_json(summary)
    md_path = save_markdown(summary)

    print(f"Saved JSON summary to {json_path}")
    print(f"Saved Markdown summary to {md_path}")