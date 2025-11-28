from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd


class DataLoadEngine(ABC):
  @abstractmethod
  def load(self, source: Path | str) -> pd.DataFrame:
    # source(파일 경로 또는 쿼리 등)를 읽어서 pandas DataFrame으로 반환
    raise NotImplementedError
