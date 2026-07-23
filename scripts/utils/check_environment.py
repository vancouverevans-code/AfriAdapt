"""
AfriAdapt Environment Check

Verifies that the Python environment and required packages
are installed correctly.
"""

import sys
import platform
import pandas as pd
import numpy as np

print("=" * 50)
print("AfriAdapt Environment Check")
print("=" * 50)
print(f"Python Version    : {sys.version}")
print(f"Python Executable : {sys.executable}")
print(f"Platform          : {platform.platform()}")
print(f"Pandas Version    : {pd.__version__}")
print(f"NumPy Version     : {np.__version__}")
print("=" * 50)
print("Environment Ready!")