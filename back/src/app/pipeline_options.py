from dataclasses import dataclass, field
from pathlib import Path
from typing import Set, Optional, List, Tuple
from app_types.pipelien import AnalysisScope, OutputTarget

@dataclass
class PipelineOptions:
  data_file: Path
  engine: str
  analysis_scope: AnalysisScope
  output_targets: Set[OutputTarget]

  json_dir: Optional[Path] = None
  charts_dir: Optional[Path] = None
  xlsx_dir: Optional[Path] = None
  frontend_json_targets: List[Tuple[Path, str, AnalysisScope]] = field(default_factory=list)
  # frontend_json_dirs: List[Path] = field(default_factory=list)
  # frontend_json_dir: Optional[Path] = None