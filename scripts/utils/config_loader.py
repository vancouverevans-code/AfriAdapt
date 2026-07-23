"""
Central configuration loader.
"""

from pathlib import Path
import yaml

CONFIG = Path("configs/config.yaml")


def load_config():

    with open(CONFIG, "r", encoding="utf-8") as file:

        return yaml.safe_load(file)


config = load_config()