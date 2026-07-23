"""
AfriAdapt Environment Check

Verifies that the local environment is correctly configured
before running any experiments.
"""

import platform
import sys
from pathlib import Path

import numpy
import pandas

from scripts.utils.paths import (
    CONFIGS,
    DATASETS,
    OUTPUTS,
    REPORTS,
    LOGS,
)


def check_directories():

    required = [
        CONFIGS,
        DATASETS,
        OUTPUTS,
        REPORTS,
        LOGS,
    ]

    print("\nProject Directories")

    for directory in required:

        exists = directory.exists()

        status = "OK" if exists else "MISSING"

        print(f"{status:8} {directory}")


def check_config():

    config = CONFIGS / "config.yaml"

    print("\nConfiguration")

    if config.exists():

        print(f"OK       {config}")

    else:

        print(f"MISSING  {config}")


def check_env():

    env = Path(".env")

    print("\nEnvironment File")

    if env.exists():

        print(f"OK       {env}")

    else:

        print(f"MISSING  {env}")


def main():

    print("=" * 60)

    print("AfriAdapt Environment Check")

    print("=" * 60)

    print(f"Python Version    : {sys.version}")

    print(f"Python Executable : {sys.executable}")

    print(f"Platform          : {platform.platform()}")

    print(f"Pandas Version    : {pandas.__version__}")

    print(f"NumPy Version     : {numpy.__version__}")

    check_directories()

    check_config()

    check_env()

    print("\n" + "=" * 60)

    print("Environment Ready!")

    print("=" * 60)


if __name__ == "__main__":

    main()