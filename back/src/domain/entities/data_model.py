from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


# QuestionData는 로드된 원본 데이터를, DatasetSummary는 최종 분석 결과를 나타냅니다.

@dataclass
class OverviewStats:
  # 데이터셋의 전반적인 개요 통계
  total_questions: int
  distinct_difficulties: int
  earliest_created_at: str
  latest_created_at: str
  days_span: int

  def to_dict(self) -> Dict[str, Any]:
    return asdict(self)


# (참고: DatasetSummary에 복잡한 메트릭스 구조를 담기 위해 임시로 Dict[str, Any]를 사용합니다.
# 이상적인 DDD는 이 Dict 내부까지 모두 별도의 Value Object로 정의하는 것입니다.)

@dataclass
class DatasetSummary:
  # 모든 주요 통계 섹션을 포함하는 최종 데이터 모델
  overview: OverviewStats
  # metrics의 모든 복잡한 구조를 담기 위해 Dict[str, Any]로 정의
  metrics: Dict[str, Any] = field(default_factory=dict)

  def to_dict(self) -> Dict[str, Any]:
    # DatasetSummary 객체를 JSON 직렬화 가능한 딕셔너리로 변환
    # 최종 JSON 구조: overview와 metrics를 평탄화하여 반환
    result = self.overview.to_dict()
    result.update(self.metrics)

    return {
      "overview": self.overview.to_dict(),
      "metrics": self.metrics,
      "timestamp": "GENERATED_TIMESTAMP_PLACEHOLDER"  # ArtifactWriter에서 업데이트될 예정
    }


@dataclass
class QuestionData:
  # 로드된 원본 데이터프레임을 캡슐화하는 도메인 객체
  df: Any  # pandas.DataFrame 대신 Any를 사용하여 pandas 의존성을 낮춥니다.
  source_name: str = "coding_questions"


@dataclass
class DifficultySummary:
  """
  난이도별 요약 통계를 저장하는 DTO (Data Transfer Object).
  """
  difficulty: str
  count: int
  avg_acceptance_rate: float
  max_submissions: int
  min_submissions: int


@dataclass
class AnalysisResult:
  # 전체 분석 결과를 캡슐화하는 핵심 아티팩트 모델.
  # 이 객체가 JSON 파일로 직렬화됨
  # 전반적인 데이터셋 메타데이터
  total_records: int
  unique_difficulties: List[str]

  # 난이도별 상세 요약 목록
  difficulty_summaries: List[DifficultySummary] = field(default_factory=list)

  # 카테고리별 분포 (dict: category -> count)
  category_distribution: Dict[str, int] = field(default_factory=dict)

  # JSON 직렬화를 위한 헬퍼 메서드
  def to_json_serializable(self) -> Dict[str, Any]:
    # AnalysisResult 객체를 JSON으로 변환 가능한 딕셔너리로 변환
    # DifficultySummary 객체 리스트를 딕셔너리 리스트로 변환
    summaries_list = [
      {
        "difficulty": s.difficulty,
        "count": s.count,
        "avg_acceptance_rate": round(s.avg_acceptance_rate, 2),
        "max_submissions": s.max_submissions,
        "min_submissions": s.min_submissions,
      }
      for s in self.difficulty_summaries
    ]

    return {
      "metadata": {
        "total_records": self.total_records,
        "unique_difficulties": self.unique_difficulties,
        "timestamp": "GENERATED_TIMESTAMP_PLACEHOLDER"  # 런타임에 삽입될 예정
      },
      "summaries": {
        "difficulty_stats": summaries_list,
        "category_distribution": self.category_distribution,
      }
    }
