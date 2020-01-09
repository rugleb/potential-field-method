from pathlib import Path

__all__ = (
    "ROOT_DIR",
    "DATA_DIR",
)

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR.joinpath("data")
