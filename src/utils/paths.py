"""
Shared path helpers for the project.
"""
from pathlib import Path

# Project root: work-intake-intelligence/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Top-level directories
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
REPORTS_DIR = PROJECT_ROOT / "reports"
TESTS_DIR = PROJECT_ROOT / "tests"

# Data subdirectories
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SYNTHETIC_DATA_DIR = DATA_DIR / "synthetic"

# Artifact subdirectories
MODELS_DIR = ARTIFACTS_DIR / "models"
METRICS_DIR = ARTIFACTS_DIR / "metrics"
PREDICTIONS_DIR = ARTIFACTS_DIR / "predictions"

# Report subdirectories
EVALUATION_REPORTS_DIR = REPORTS_DIR / "evaluation"
MONITORING_REPORTS_DIR = REPORTS_DIR / "monitoring"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"


def ensure_project_dirs() -> None:
    """Create key project directories if they do not already exist."""
    dirs_to_create = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        SYNTHETIC_DATA_DIR,
        MODELS_DIR,
        METRICS_DIR,
        PREDICTIONS_DIR,
        EVALUATION_REPORTS_DIR,
        MONITORING_REPORTS_DIR,
        SCREENSHOTS_DIR,
        TESTS_DIR,
    ]

    for directory in dirs_to_create:
        directory.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    ensure_project_dirs()
    print(f"Project root: {PROJECT_ROOT}")
    print("Verified project directories.")