from .base import DataLoadEngine
import pandas as pd
from pathlib import Path


class CSVDataEngine(DataLoadEngine):
  # CSV 파일을 읽어서 DataFrame으로 반환
  def __init__(self, encoding: str = "utf-8", sep: str = ","):
    self.encoding = encoding
    self.sep = sep

  def load(self, source: Path | str) -> pd.DataFrame:
    path = Path(source)
    df = pd.read_csv(path, encoding=self.encoding, sep=self.sep)
    return df
