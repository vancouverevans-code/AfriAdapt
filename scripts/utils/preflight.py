"""
AfriAdapt Preflight Checks
"""

from pathlib import Path


REQUIRED = [
    Path("configs/config.yaml"),
    Path(".env"),
    Path("datasets/raw"),
]


def main():

    missing = []

    for item in REQUIRED:

        if not item.exists():

            missing.append(item)

    if missing:

        print("\nMissing required resources:")

        for item in missing:

            print(f" - {item}")

        raise FileNotFoundError(
            "Preflight checks failed."
        )

    print("Preflight checks passed.")


if __name__ == "__main__":
    main()