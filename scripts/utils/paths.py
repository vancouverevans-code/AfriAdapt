"""
AfriAdapt Project Paths

Centralizes every project path so that the
rest of the project never hardcodes folders.
"""

from pathlib import Path

# ----------------------------------------------------
# Project Root
# ----------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

# ----------------------------------------------------
# Main Folders
# ----------------------------------------------------

CONFIGS = PROJECT_ROOT / "configs"

DATASETS = PROJECT_ROOT / "datasets"

OUTPUTS = PROJECT_ROOT / "outputs"

REPORTS = PROJECT_ROOT / "reports"

LOGS = PROJECT_ROOT / "logs"

MODELS = PROJECT_ROOT / "models"

DOCS = PROJECT_ROOT / "docs"

EXPERIMENTS = PROJECT_ROOT / "experiments"

# ----------------------------------------------------
# Dataset Folders
# ----------------------------------------------------

RAW_DATA = DATASETS / "raw"

GENERATED_DATA = DATASETS / "generated"

BENCHMARK_DATA = DATASETS / "benchmark"

# ----------------------------------------------------
# Output Files
# ----------------------------------------------------

BENCHMARK_OUTPUT = (
    BENCHMARK_DATA /
    "afribench_candidates.jsonl"
)

BENCHMARK_FINAL = (
    BENCHMARK_DATA /
    "afribench_v1.jsonl"
)

REPORT_OUTPUT = (
    REPORTS /
    "evaluation_report.json"
)

# ----------------------------------------------------
# Auto-create folders
# ----------------------------------------------------

DIRECTORIES = [

    CONFIGS,

    DATASETS,

    OUTPUTS,

    REPORTS,

    LOGS,

    MODELS,

    DOCS,

    EXPERIMENTS,

    RAW_DATA,

    GENERATED_DATA,

    BENCHMARK_DATA,

]

for directory in DIRECTORIES:

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )