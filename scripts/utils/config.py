"""
AfriAdapt Configuration Loader
"""

from pathlib import Path
import yaml

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Correct configuration folder
CONFIG_PATH = PROJECT_ROOT / "configs" / "config.yaml"


def load_config():
    """
    Load the project configuration.
    """

    if not CONFIG_PATH.exists():
        raise FileNotFoundError(
            f"Configuration file not found:\n{CONFIG_PATH}"
        )

    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)