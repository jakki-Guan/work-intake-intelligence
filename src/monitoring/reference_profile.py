from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any


def load_prediction_logs(
    log_dir: str = "data/monitoring/prediction_logs",
    limit: int | None = None,
) -> list[dict[str, Any]]:
    path = Path(log_dir)
    rows: list[dict[str, Any]] = []

    if not path.exists():
        return rows

    for file_path in sorted(path.glob("*.jsonl")):
        with file_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))

    if limit is not None:
        rows = rows[-limit:]

    return rows

def percentile(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = int((len(values) - 1) * p)
    return float(values[idx])


def build_reference_profile(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {
            "n_predictions": 0,
            "avg_text_length_chars": 0.0,
            "avg_text_length_words": 0.0,
            "sla_at_risk_rate": 0.0,
            "routing_low_confidence_rate": 0.0,
            "p95_latency_ms": 0.0,
        }

    char_lengths = [row["input_profile"]["text_length_chars"] for row in rows]
    word_lengths = [row["input_profile"]["text_length_words"] for row in rows]
    sla_probs = [row["sla_prediction"]["probability"] for row in rows]
    routing_confidences = [row["routing_prediction"]["confidence"] for row in rows]
    latencies = [row["latency_ms"] for row in rows]

    return {
        "n_predictions": len(rows),
        "avg_text_length_chars": round(mean(char_lengths), 2),
        "avg_text_length_words": round(mean(word_lengths), 2),
        "sla_at_risk_rate": round(mean(1.0 if p >= 0.5 else 0.0 for p in sla_probs), 4),
        "routing_low_confidence_rate": round(mean(1.0 if c < 0.45 else 0.0 for c in routing_confidences), 4),
        "p95_latency_ms": round(percentile(latencies, 0.95), 2),
    }


def save_reference_profile(
    profile: dict[str, Any],
    output_path: str = "data/monitoring/reference/reference_profile.json",
) -> str:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile, indent=2), encoding="utf-8")
    return str(path)


if __name__ == "__main__":
    rows = load_prediction_logs()
    profile = build_reference_profile(rows)
    out = save_reference_profile(profile)
    print(f"Saved reference profile to {out}")