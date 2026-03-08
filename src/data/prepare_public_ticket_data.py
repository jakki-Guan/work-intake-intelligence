from __future__ import annotations

import random
from typing import Optional

import pandas as pd

from src.utils.paths import RAW_DATA_DIR, ensure_project_dirs


RAW_INPUT_FILE = RAW_DATA_DIR / "public_tickets_multi_lang_20k.csv"
STANDARDIZED_OUTPUT_FILE = RAW_DATA_DIR / "public_tickets_standardized_v1.csv"


def load_raw_public_data() -> pd.DataFrame:
    """Load the raw public ticket dataset from the local raw data folder."""
    return pd.read_csv(RAW_INPUT_FILE)


def filter_english_only(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only English rows for the baseline version."""
    if "language" not in df.columns:
        raise ValueError("Expected column 'language' was not found in the raw dataset.")

    df = df.copy()
    df["language"] = df["language"].astype(str).str.lower().str.strip()
    return df[df["language"] == "en"].copy()


def normalize_priority(value: Optional[str]) -> str:
    """Normalize priority values into low / medium / high."""
    if pd.isna(value):
        return "medium"

    text = str(value).strip().lower()

    if text in {"low", "minor", "p3", "3"}:
        return "low"
    if text in {"medium", "normal", "moderate", "p2", "2"}:
        return "medium"
    if text in {"high", "urgent", "critical", "p1", "1"}:
        return "high"

    return "medium"


def sample_channel() -> str:
    """Sample a synthetic intake channel."""
    return random.choices(
        population=["email", "portal", "chat"],
        weights=[0.50, 0.35, 0.15],
        k=1,
    )[0]


def sample_requester_type() -> str:
    """Sample a synthetic requester type."""
    return random.choices(
        population=["internal", "external", "vip"],
        weights=[0.70, 0.25, 0.05],
        k=1,
    )[0]


def sample_created_hour() -> int:
    """Sample an hour of day for request creation."""
    return random.randint(0, 23)


def derive_sla_risk(
    routing_queue: str,
    priority: str,
    channel: str,
    requester_type: str,
    created_hour: int,
) -> int:
    """
    Create a reproducible proxy SLA risk label.

    This is NOT a real historical SLA breach label.
    It is a project-defined proxy based on business-style heuristics.
    """
    score = 0.0

    # Priority still matters most, but less aggressively
    if priority == "high":
        score += 1.5
    elif priority == "medium":
        score += 0.75

    # Queue effect
    if routing_queue in {"service outages and maintenance", "technical support", "it support"}:
        score += 1.0
    elif routing_queue in {"product support", "billing and payments"}:
        score += 0.5

    # Channel effect: keep email higher, but reduce the gap
    if channel == "email":
        score += 0.5
    elif channel == "chat":
        score += 0.2

    # Requester effect
    if requester_type == "external":
        score += 0.75
    elif requester_type == "vip":
        score -= 0.5

    # Off-hours effect
    if created_hour < 8 or created_hour > 18:
        score += 1.0

    # Small randomness to avoid a rigid deterministic label
    score += random.uniform(-0.5, 0.75)

    return 1 if score >= 3.0 else 0


def clean_text(value: Optional[str]) -> str:
    """Basic cleanup for raw text fields."""
    if pd.isna(value):
        return ""
    return " ".join(str(value).strip().split())


def build_standardized_dataset(df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """Map raw public ticket fields into the project's unified schema."""
    random.seed(seed)

    required_columns = ["subject", "body", "queue", "priority", "type", "language"]
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns in raw dataset: {missing}")

    df = df.copy().reset_index(drop=True)

    df["title"] = df["subject"].apply(clean_text)
    df["description"] = df["body"].apply(clean_text)
    df["routing_queue"] = df["queue"].astype(str).str.strip().str.lower()
    df["priority"] = df["priority"].apply(normalize_priority)
    df["request_type"] = df["type"].astype(str).str.strip().str.lower()
    df["language"] = df["language"].astype(str).str.strip().str.lower()

    df["ticket_id"] = [f"PUB-{i:05d}" for i in range(1, len(df) + 1)]
    df["channel"] = [sample_channel() for _ in range(len(df))]
    df["requester_type"] = [sample_requester_type() for _ in range(len(df))]
    df["created_hour"] = [sample_created_hour() for _ in range(len(df))]

    df["sla_risk"] = df.apply(
        lambda row: derive_sla_risk(
            routing_queue=row["routing_queue"],
            priority=row["priority"],
            channel=row["channel"],
            requester_type=row["requester_type"],
            created_hour=int(row["created_hour"]),
        ),
        axis=1,
    )

    standardized_df = df[
        [
            "ticket_id",
            "title",
            "description",
            "channel",
            "priority",
            "requester_type",
            "created_hour",
            "routing_queue",
            "request_type",
            "language",
            "sla_risk",
        ]
    ].copy()

    return standardized_df


def main() -> None:
    ensure_project_dirs()

    raw_df = load_raw_public_data()
    english_df = filter_english_only(raw_df)
    standardized_df = build_standardized_dataset(english_df, seed=42)

    standardized_df.to_csv(STANDARDIZED_OUTPUT_FILE, index=False)

    print(f"Read raw file from: {RAW_INPUT_FILE}")
    print(f"Saved standardized file to: {STANDARDIZED_OUTPUT_FILE}")
    print(f"Raw shape: {raw_df.shape}")
    print(f"English-only shape: {english_df.shape}")
    print(f"Standardized shape: {standardized_df.shape}")
    print(standardized_df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()