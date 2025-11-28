from dataclasses import dataclass
from pathlib import Path


@dataclass
class PipelineOptions:
  data_file: Path
  generate_charts: bool = True
  generate_excel: bool = True
  engine: str = "csv"

  # TODO: 난이도/태그 필터, preset 같은 것 여기로 확장 가능
