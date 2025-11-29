from __future__ import annotations

from collections import Counter
from typing import Any, Dict, Sequence

import pandas as pd

from infrastructure.logging import get_logger
from domain.entities.data_model import OverviewStats
from constants.analysis import (
  EXAMPLE_BINS,
  EXAMPLE_LABELS,
  TEST_CASE_BINS,
  TEST_CASE_LABELS,
  DESCRIPTION_LENGTH_BINS,
  DESCRIPTION_LENGTH_LABELS,
  CONSTRAINTS_BINS,
  CONSTRAINTS_LABELS,
)
from domain.service.metrics_scopes import (
  enrich_dataframe,
  count_description_templates
)

logger = get_logger(__name__)


# =================================================================
# 집계용 헬퍼 함수 (Aggregation Helpers)
# 이 함수들은 Row 단위 처리가 아니라 Column(Series) 단위 집계
# =================================================================
def _distribution(series: pd.Series) -> Dict[str, Dict[str, float]]:
  counts = series.value_counts()
  total = counts.sum() or 1
  percentages = (counts / total * 100).round(2)
  return {"counts": counts.to_dict(), "percentages": percentages.to_dict()}


def _bucket_counts(series: pd.Series, bins: Sequence[float], labels: list[str]) -> Dict[str, int]:
  categories = pd.cut(series, bins=bins, labels=labels, include_lowest=True, right=False)
  return categories.value_counts().reindex(labels, fill_value=0).to_dict()


def _top_tags(tags_series: pd.Series, limit: int = 10) -> Dict[str, int]:
  counter: Counter[str] = Counter()
  for tags in tags_series:
    counter.update(tags)
  return dict(counter.most_common(limit))


def _aggregate_over_time(df: pd.DataFrame) -> list[dict]:
  counts = (
    df.dropna(subset=["created_date"])
    .groupby("created_date")
    .size()
    .sort_index()
  )
  return [{"date": str(date), "count": int(count)} for date, count in counts.items()]


def _difficulty_over_time(df: pd.DataFrame) -> list[dict]:
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
  pivot = pd.crosstab(df[index_col], df[column_col])
  return {str(idx): {str(col): int(pivot.at[idx, col]) for col in pivot.columns} for idx in pivot.index}


# =================================================================
# Main Public API
# =================================================================
def compute_statistics(df: pd.DataFrame) -> Dict[str, Any]:
  if df is None or df.empty:
    logger.error("Input DataFrame is empty or None.")
    raise ValueError("Input DataFrame is empty or None")

  logger.info("Computing full dataset statistics.")

  # 1. 데이터 전처리 (Scopes 모듈 위임)
  data = enrich_dataframe(df)

  # 2. Overview Stats 계산
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

  # 3. Metrics 상세 통계 계산
  metrics: Dict[str, Any] = {
    # 분포 통계
    "difficulty_distribution": _distribution(data["difficulty_level"]),
    "algorithm_category_distribution": _distribution(data["algorithm_category"]),
    "input_type_distribution": _distribution(data["input_type"]),
    "output_type_distribution": _distribution(data["output_type"]),
    "negative_one_output_problems_ratio": _distribution(data["returns_negative_one"]),
    "top_tags_distribution": _top_tags(data["problem_tags"], limit=10),

    # 평균 통계
    "avg_description_length_by_difficulty": data.groupby("difficulty_level")["description_length"].mean().round(2).to_dict(),
    "avg_test_cases_by_difficulty": data.groupby("difficulty_level")["num_test_cases"].mean().round(2).to_dict(),
    "example_testcase_by_difficulty": data.groupby("difficulty_level")[
      ["num_examples", "num_test_cases"]
    ].mean().round(2).to_dict(orient="index"),

    # 버킷(구간) 통계 - Config 상수 활용
    "example_count_distribution": _bucket_counts(data["num_examples"], EXAMPLE_BINS, EXAMPLE_LABELS),
    "test_case_count_distribution": _bucket_counts(data["num_test_cases"], TEST_CASE_BINS, TEST_CASE_LABELS),
    "description_length_bucket_distribution": _bucket_counts(data["description_length"], DESCRIPTION_LENGTH_BINS, DESCRIPTION_LENGTH_LABELS),
    "constraints_count_distribution": _bucket_counts(data["constraints_count"], CONSTRAINTS_BINS, CONSTRAINTS_LABELS),

    # 시계열 통계
    "problems_per_day": _aggregate_over_time(data),
    "difficulty_over_time": _difficulty_over_time(data),

    # 교차 분석 (Matrix)
    "difficulty_algorithm_matrix": _matrix(data, "difficulty_level", "algorithm_category"),
    "difficulty_input_type_matrix": _matrix(data, "difficulty_level", "input_type"),

    # 기타 분석
    "duplicate_title_count": int(data["title"].str.lower().str.strip().duplicated().sum()),
    "description_template_usage": count_description_templates(data["description"]),
  }

  result = {"overview": overview.to_dict(), "metrics": metrics}
  logger.info("Finished computing statistics.")
  return result
