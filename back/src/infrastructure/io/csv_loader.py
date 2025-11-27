from pathlib import Path
import pandas as pd
from core.config import ENCODING

def load_csv(path: Path) -> pd.DataFrame:
  if not path.exists():
    raise FileNotFoundError(f"CSV file not found: {path}")

  df = pd.read_csv(path, encoding=ENCODING)
  return df
