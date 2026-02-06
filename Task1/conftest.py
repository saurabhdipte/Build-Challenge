import sys
from pathlib import Path

# Add Task1/src to PYTHONPATH so "library_system" imports work in tests
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
