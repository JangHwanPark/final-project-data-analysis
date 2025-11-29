from dataclasses import dataclass
from pathlib import Path
from typing import Set
from app_types.pipelien import AnalysisScope, OutputTarget

@dataclass
class PipelineOptions:
  data_file: Path
  engine: str
  generate_charts: bool
  generate_excel: bool

  # TODO: 난이도/태그 필터, preset 같은 것 여기로 확장 가능
  analysis_scope: AnalysisScope
  output_targets: Set[OutputTarget]