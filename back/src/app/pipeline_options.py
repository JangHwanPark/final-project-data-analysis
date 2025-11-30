from dataclasses import dataclass, field
from pathlib import Path
from typing import Set, Optional, List

from app_types.pipelien import AnalysisScope, OutputTarget
from constants.path import FrontendPaths


@dataclass
class FrontendJsonTarget:
  # path: Path
  target_dir: Path
  filename: str
  scope: AnalysisScope
  keys: Optional[list[str]] = None


@dataclass
class PipelineOptions:
  data_file: Path
  engine: str
  analysis_scope: AnalysisScope
  output_targets: Set[OutputTarget]

  json_dir: Optional[Path] = None
  charts_dir: Optional[Path] = None
  xlsx_dir: Optional[Path] = None
  frontend_json_targets: List[FrontendJsonTarget] = field(default_factory=list)


# ====================================================
# 탭에 매핑되는 메트릭 키 정의
# ====================================================
def _tab_metric_keys() -> dict[str, list[str]]:
  return {
    "overview": [
      "total_questions",
      "days_span",
      "latest_created_at",
      "earliest_created_at",
      "difficulty_distribution",
      "problems_per_day",
    ],
    "difficulty": [
      "difficulty_distribution",
      "difficulty_over_time",
      "avg_description_length_by_difficulty",
      "avg_test_cases_by_difficulty",
    ],
    "tags": [
      "top_tags_distribution",
      "algorithm_category_distribution",
      "input_type_distribution",
    ],
    "structure": [
      "description_length_bucket_distribution",
      "constraints_count_distribution",
      "example_count_distribution",
      "test_case_count_distribution",
    ],
  }


# ====================================================
# 탭 별로 분리된 JSON 산출물을
# 프론트 경로에 저장하기 위한 기본 설정을 반환
# ====================================================
def default_frontend_targets(
        analysis_scope: AnalysisScope,
        custom_keys: Optional[List[str]] = None
) -> list[FrontendJsonTarget]:
  # FrontendPaths.SHARED_DATA_DIR가 존재하지 않으면 생성
  base_dir = FrontendPaths.SHARED_DATA_DIR
  base_dir.mkdir(parents=True, exist_ok=True)

  metric_keys = _tab_metric_keys()
  targets: list[FrontendJsonTarget] = []

  # RAW/DOWNLOAD 파일 (모든 범위에서 FULL로 저장)
  # keys=None이면 JsonExporter가 전체 데이터를 저장
  targets.append(FrontendJsonTarget(
    target_dir=base_dir,
    filename="summary-full.json",
    scope=AnalysisScope.FULL,
    keys=None
  ))

  # FULL 범위: 모든 탭별 파일 생성 + 다운로드용 RAW 파일
  if analysis_scope == AnalysisScope.FULL:
    targets.extend([
      FrontendJsonTarget(base_dir, "overview.json", AnalysisScope.FULL, metric_keys["overview"]),
      FrontendJsonTarget(base_dir, "difficulty.json", AnalysisScope.FULL, metric_keys["difficulty"]),
      FrontendJsonTarget(base_dir, "tags.json", AnalysisScope.FULL, metric_keys["tags"]),
      FrontendJsonTarget(base_dir, "structure.json", AnalysisScope.FULL, metric_keys["structure"]),
    ])

  # BASIC 범위: overview 파일만 생성 (가장 가벼운 기본)
  elif analysis_scope == AnalysisScope.BASIC:
    targets.append(FrontendJsonTarget(base_dir, "overview.json", AnalysisScope.BASIC, metric_keys["overview"]))

  # CUSTOM 범위: custom_keys를 사용하여 단일 파일 생성 (현재는 구현의 복잡성 때문에 단일 파일로 제한)
  elif analysis_scope == AnalysisScope.CUSTOM and custom_keys:
    targets.append(FrontendJsonTarget(base_dir, "custom_report.json", AnalysisScope.CUSTOM, custom_keys))

  return targets