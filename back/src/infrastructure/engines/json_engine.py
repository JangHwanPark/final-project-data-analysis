from .base import DataLoadEngine
import pandas as pd
from pathlib import Path
import json


class JSONDataEngine(DataLoadEngine):
  # JSON 파일(레코드 배열 형태)을 읽어서 DataFrame으로 변환
  def load(self, source: Path | str) -> pd.DataFrame:
    path = Path(source)

    with path.open("r", encoding="utf-8") as f:
      data = json.load(f)

    # TODO: data가 리스트[dict, dict, ...] 라는 가정
    df = pd.DataFrame(data)
    return df
