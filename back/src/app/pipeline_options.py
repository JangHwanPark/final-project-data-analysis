from dataclasses import dataclass
from pathlib import Path
from typing import Set, Optional
from app_types.pipelien import AnalysisScope, OutputTarget

@dataclass
class PipelineOptions:
  data_file: Path
  engine: str
  generate_charts: bool
  generate_excel: bool
  analysis_scope: AnalysisScope
  output_targets: Set[OutputTarget]
  json_dir: Optional[Path] = None
  charts_dir: Optional[Path] = None
  xlsx_dir: Optional[Path] = None
  summaries_dir: Optional[Path] = None