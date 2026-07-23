"""
Configuration loader for AfriAdapt.
"""

from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).resolve().parents[2] / "config" / "config.yaml"


def load_config():
    """Load the project configuration."""
    with open(CONFIG_PATH, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


if __name__ == "__main__":
    config = load_config()
    print(config)