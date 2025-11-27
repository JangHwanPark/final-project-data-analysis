from __future__ import annotations

import json
import re
from collections import Counter
from typing import Any, Dict, List, Sequence

import pandas as pd

# --- Infrastructure Layer: 로거 임포트 ---
from infrastructure.logging import get_logger

# --- Domain Layer: 상수 및 엔티티 임포트 ---
# 분석 상수 (분류 규칙) 임포트
from domain.analysis_constants import (
  ALGORITHM_CATEGORY_KEYWORDS,
  INPUT_TYPE_KEYWORDS,
  TAG_KEYWORDS,
  OUTPUT_TYPE_MAPPINGS,
  DESCRIPTION_TEMPLATE_PATTERNS,
  EXAMPLE_BINS, EXAMPLE_LABELS,
  TEST_CASE_BINS, TEST_CASE_LABELS,
  DESCRIPTION_LENGTH_BINS, DESCRIPTION_LENGTH_LABELS,
  CONSTRAINTS_BINS, CONSTRAINTS_LABELS,
)

# 도메인 엔티티 (데이터 구조) 임포트
from domain.entities.data_model import (
  OverviewStats,
  DatasetSummary,
)

logger = get_logger(__name__)


# =================================================================
# Private Helper Functions for Data Preparation and Metrics Calculation
# (These functions belong here as they implement the metrics service's logic)
# =================================================================

def _safe_length(series: pd.Series) -> pd.Series:
  # 시리즈의 널(null) 값을 빈 문자열로 대체하여 문자열 길이를 안전하게 계산
  return series.fillna("").astype(str).str.len()


def _normalize_difficulty(series: pd.Series) -> pd.Series:
  # 난이도 문자열을 정규화(Unknown 처리 및 Title Case 변환)
  return series.fillna("Unknown").astype(str).str.title()


def _load_json_array(value: Any) -> list:
  # 데이터프레임 셀의 JSON 문자열을 파싱하여 리스트를 반환
  if isinstance(value, list):
    return value
  if value is None or (isinstance(value, float) and pd.isna(value)):
    return []
  if isinstance(value, str):
    try:
      parsed = json.loads(value)
      if isinstance(parsed, list):
        return parsed
    except json.JSONDecodeError:
      logger.warning(f"Failed to decode JSON array string: {value[:50]}...")
      return []
  return []


def _collect_text(row: pd.Series) -> str:
  # 제목과 설명을 결합하여 태깅을 위한 단일 텍스트 문자열을 생성
  parts = [row.get("title", ""), row.get("description", "")]
  return " ".join(str(p) for p in parts if p)


def _assign_algorithm_category(text: str) -> str:
  # 텍스트 내 키워드 매칭을 통해 알고리즘 카테고리를 할당
  text_lower = text.lower()
  for category, keywords in ALGORITHM_CATEGORY_KEYWORDS.items():
    if any(keyword in text_lower for keyword in keywords):
      return category
  return "Uncategorized"


def _assign_input_type(text: str) -> str:
  # 텍스트 내 키워드 매칭을 통해 입력 데이터 타입을 할당
  text_lower = text.lower()
  for input_type, keywords in INPUT_TYPE_KEYWORDS.items():
    if any(keyword in text_lower for keyword in keywords):
      return input_type
  return "Mixed/Other"


def _extract_problem_tags(text: str) -> list[str]:
  # 텍스트 내 키워드 매칭을 통해 문제 태그 리스트를 추출
  text_lower = text.lower()
  tags: list[str] = []
  for tag, keywords in TAG_KEYWORDS.items():
    if any(keyword in text_lower for keyword in keywords):
      tags.append(tag)
  return tags if tags else ["uncategorized"]


def _infer_output_type(cases: Sequence[dict]) -> str:
  """테스트 케이스의 예상 출력을 기반으로 출력 데이터 타입을 추론합니다 (상수 사용)."""
  for case in cases:
    expected = case.get("expected_output") if isinstance(case, dict) else None
    if expected is None:
      continue
    for candidate_type, label in OUTPUT_TYPE_MAPPINGS:
      if isinstance(expected, candidate_type):
        return label
  return "Unknown"


def _flag_negative_one(text: str, cases: Sequence[dict]) -> bool:
  # 텍스트나 예상 출력에 -1이 포함되어 있는지 확인
  if "-1" in text:
    return True
  for case in cases:
    if isinstance(case, dict) and case.get("expected_output") == -1:
      return True
  return False


def _description_templates(series: pd.Series) -> Dict[str, int]:
  # 설명 텍스트에서 정의된 템플릿 패턴의 사용 빈도를 계산
  counts: Dict[str, int] = {name: 0 for name in DESCRIPTION_TEMPLATE_PATTERNS}
  for value in series.fillna(""):
    for name, pattern in DESCRIPTION_TEMPLATE_PATTERNS.items():
      if pattern.search(str(value)):
        counts[name] += 1
  return counts


def _prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
  # 원본 데이터프레임에 전처리 및 특징 추출을 적용하여 보강된 데이터프레임을 반환
  logger.info("Starting DataFrame enrichment and feature engineering.")
  enriched = df.copy()

  # 정규화 및 길이 계산
  enriched["difficulty_level"] = _normalize_difficulty(enriched.get("difficulty_level", pd.Series(dtype=str)))
  enriched["title"] = enriched.get("Title", enriched.get("title", "")).fillna("")
  enriched["description"] = enriched.get("Description", enriched.get("description", "")).fillna("")
  enriched["description_length"] = _safe_length(enriched["description"])

  # JSON 파싱
  enriched["examples_parsed"] = enriched.get("Examples", enriched.get("examples", pd.Series(dtype=object))).apply(_load_json_array)
  enriched["test_cases_parsed"] = enriched.get("Test Cases", enriched.get("test_cases", pd.Series(dtype=object))).apply(_load_json_array)
  enriched["constraints_parsed"] = enriched.get("Constraints", enriched.get("constraints", pd.Series(dtype=object))).apply(_load_json_array)

  # 개수 계산
  enriched["num_examples"] = enriched["examples_parsed"].apply(len)
  enriched["num_test_cases"] = enriched["test_cases_parsed"].apply(len)
  enriched["constraints_count"] = enriched["constraints_parsed"].apply(len)

  # 텍스트 기반 특징 추출
  enriched["combined_text"] = enriched.apply(_collect_text, axis=1)
  enriched["algorithm_category"] = enriched["combined_text"].apply(_assign_algorithm_category)
  enriched["input_type"] = enriched["combined_text"].apply(_assign_input_type)
  enriched["problem_tags"] = enriched["combined_text"].apply(_extract_problem_tags)
  enriched["output_type"] = enriched["test_cases_parsed"].apply(_infer_output_type)

  # 특정 특징 플래그
  enriched["returns_negative_one"] = enriched.apply(
    lambda row: _flag_negative_one(str(row.get("combined_text", "")), row.get("test_cases_parsed", [])),
    axis=1,
  )

  # 시간 기반 특징
  created = pd.to_datetime(enriched.get("CreatedAt", enriched.get("created_at")), errors="coerce")
  enriched["created_date"] = created.dt.date

  logger.info("DataFrame enrichment complete.")
  return enriched


def _distribution(series: pd.Series) -> Dict[str, Dict[str, float]]:
  # 시리즈의 값 분포 (개수 및 백분율)를 계산
  counts = series.value_counts()
  total = counts.sum() or 1
  percentages = (counts / total * 100).round(2)
  return {"counts": counts.to_dict(), "percentages": percentages.to_dict()}


def _bucket_counts(series: pd.Series, bins: Sequence[float], labels: list[str]) -> Dict[str, int]:
  # 연속적인 데이터를 정의된 버킷으로 나누어 개수를 계산
  categories = pd.cut(series, bins=bins, labels=labels, include_lowest=True, right=False)
  # 모든 레이블에 대해 개수가 0인 경우를 포함하여 반환
  return categories.value_counts().reindex(labels, fill_value=0).to_dict()


def _top_tags(tags_series: pd.Series, limit: int = 10) -> Dict[str, int]:
  # 가장 많이 사용된 태그의 빈도를 계산
  counter: Counter[str] = Counter()
  for tags in tags_series:
    counter.update(tags)
  return dict(counter.most_common(limit))


def _aggregate_over_time(df: pd.DataFrame) -> list[dict]:
  # 날짜별 문제 생성 개수를 집계
  counts = (
    df.dropna(subset=["created_date"])
    .groupby("created_date")
    .size()
    .sort_index()
  )
  return [{"date": str(date), "count": int(count)} for date, count in counts.items()]


def _difficulty_over_time(df: pd.DataFrame) -> list[dict]:
  # 날짜별 난이도별 문제 개수를 집계
  grouped = (
    df.dropna(subset=["created_date"])
    .groupby(["created_date", "difficulty_level"])
    .size()
    .unstack(fill_value=0)
    .sort_index()
  )
  records: list[dict] = []
  for date, row in grouped.iterrows():
    payload = {"date": str(date)}
    payload.update({str(col): int(row[col]) for col in row.index})
    records.append(payload)
  return records


def _matrix(df: pd.DataFrame, index_col: str, column_col: str) -> Dict[str, Dict[str, int]]:
  # 두 범주형 변수 간의 교차표(Cross-tabulation)를 계산
  pivot = pd.crosstab(df[index_col], df[column_col])
  return {str(idx): {str(col): int(pivot.at[idx, col]) for col in pivot.columns} for idx in pivot.index}


def compute_statistics(df: pd.DataFrame) -> Dict[str, Any]:
  # 코딩 질문 데이터셋에서 주요 통계 지표를 계산하고 JSON serializable 딕셔너리를 반환
  if df is None or df.empty:
    logger.error("Input DataFrame is empty or None.")
    raise ValueError("Input DataFrame is empty or None")

  logger.info("Computing full dataset statistics.")
  data = _prepare_dataframe(df)

  # Overview Stats (개요) 계산
  created = pd.to_datetime(data.get("CreatedAt", data.get("created_at")), errors="coerce")
  earliest = created.min()
  latest = created.max()
  overview = OverviewStats(
    total_questions=int(len(data)),
    distinct_difficulties=int(data["difficulty_level"].nunique()),
    earliest_created_at=earliest.isoformat() if pd.notna(earliest) else "N/A",
    latest_created_at=latest.isoformat() if pd.notna(latest) else "N/A",
    days_span=int((latest - earliest).days) if pd.notna(earliest) and pd.notna(latest) else 0,
  )

  # Metrics (상세 통계) 계산
  metrics: Dict[str, Any] = {
    "difficulty_distribution": _distribution(data["difficulty_level"]),
    "avg_description_length_by_difficulty": data.groupby("difficulty_level")["description_length"].mean().round(2).to_dict(),
    "avg_test_cases_by_difficulty": data.groupby("difficulty_level")["num_test_cases"].mean().round(2).to_dict(),
    "algorithm_category_distribution": _distribution(data["algorithm_category"]),
    "input_type_distribution": _distribution(data["input_type"]),
    "top_tags_distribution": _top_tags(data["problem_tags"], limit=10),

    # 상수 파일에서 임포트된 버킷 설정 사용
    "example_count_distribution": _bucket_counts(
      data["num_examples"],
      bins=EXAMPLE_BINS,
      labels=EXAMPLE_LABELS,
    ),
    "test_case_count_distribution": _bucket_counts(
      data["num_test_cases"],
      bins=TEST_CASE_BINS,
      labels=TEST_CASE_LABELS,
    ),
    "example_testcase_by_difficulty": data.groupby("difficulty_level")[
      ["num_examples", "num_test_cases"]
    ].mean().round(2).to_dict(orient="index"),
    "description_length_bucket_distribution": _bucket_counts(
      data["description_length"],
      bins=DESCRIPTION_LENGTH_BINS,
      labels=DESCRIPTION_LENGTH_LABELS,
    ),
    "constraints_count_distribution": _bucket_counts(
      data["constraints_count"],
      bins=CONSTRAINTS_BINS,
      labels=CONSTRAINTS_LABELS,
    ),

    "problems_per_day": _aggregate_over_time(data),
    "difficulty_over_time": _difficulty_over_time(data),

    "output_type_distribution": _distribution(data["output_type"]),
    "negative_one_output_problems_ratio": _distribution(data["returns_negative_one"]),

    "difficulty_algorithm_matrix": _matrix(data, "difficulty_level", "algorithm_category"),
    "difficulty_input_type_matrix": _matrix(data, "difficulty_level", "input_type"),

    "duplicate_title_count": int(data["title"].str.lower().str.strip().duplicated().sum()),
    "description_template_usage": _description_templates(data["description"]),
  }

  # DatasetSummary DTO를 사용하여 최종 결과를 캡슐화합니다.
  # DatasetSummary는 to_dict() 메서드에서 Overview와 Metrics를 구조화합니다.
  # 참고: 현재 DatasetSummary DTO는 모든 metrics를 포함하지 않으므로, 딕셔너리로 직접 반환합니다.
  # 만약 DatasetSummary DTO를 사용하려면, 모든 metrics 필드를 DatasetSummary에 추가해야 합니다.
  # 현재는 요청된 딕셔너리 구조를 맞추기 위해 DTO 대신 딕셔너리를 직접 구성합니다.
  result = {"overview": overview.to_dict(), "metrics": metrics}
  logger.info("Finished computing statistics.")
  return result
