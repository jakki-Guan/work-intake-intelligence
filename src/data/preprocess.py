"""
Preprocessing utilities for work-intake data.
"""
from __future__ import annotations

import pandas as pd

from src.utils.paths import (
    SYNTHETIC_DATA_DIR,
    PROCESSED_DATA_DIR,
    ensure_project_dirs,
    RAW_DATA_DIR,
)


def normalize_text(text: str) -> str:
    """Apply lightweight normalization for modeling text."""
    text = str(text).strip().lower()
    text = " ".join(text.split())
    return text


def build_model_input(df: pd.DataFrame) -> pd.DataFrame:
    """Create the minimum processed dataset for baseline modeling."""
    df = df.copy()

    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")

    df["text"] = (df["title"] + " " + df["description"]).apply(normalize_text)

    model_df = df[
        [
            "ticket_id",
            "text",
            "channel",
            "priority",
            "requester_type",
            "created_hour",
            "routing_queue",
            "sla_risk",
        ]
    ].copy()

    return model_df


def main() -> None:
    ensure_project_dirs()

    input_path = RAW_DATA_DIR / "public_tickets_standardized_v1.csv"
    output_path = PROCESSED_DATA_DIR / "work_intake_model_input_v2.csv"

    df = pd.read_csv(input_path)
    model_df = build_model_input(df)
    model_df.to_csv(output_path, index=False)

    print(f"Read input from: {input_path}")
    print(f"Saved processed data to: {output_path}")
    print(f"Shape: {model_df.shape}")
    print(model_df.head(5).to_string(index=False))


if __name__ == "__main__":
    main()