from __future__ import annotations

import json
from typing import Any, Dict, Sequence
import pandas as pd

from infrastructure.logging import get_logger
from constants.analysis import (
  ALGORITHM_CATEGORY_KEYWORDS,
  INPUT_TYPE_KEYWORDS,
  TAG_KEYWORDS,
  OUTPUT_TYPE_MAPPINGS,
  DESCRIPTION_TEMPLATE_PATTERNS,
  DEFAULT_NA_VALUE,
)

logger = get_logger(__name__)


def _safe_length(series: pd.Series) -> pd.Series:
  return series.fillna("").astype(str).str.len()


def _normalize_difficulty(series: pd.Series) -> pd.Series:
  return series.fillna(DEFAULT_NA_VALUE).astype(str).str.title()


def _load_json_array(value: Any) -> list:
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
      # 로깅 레벨을 조절하거나 필요시 로그를 남깁니다.
      return []
  return []


def _collect_text(row: pd.Series) -> str:
  parts = [row.get("title", ""), row.get("description", "")]
  return " ".join(str(p) for p in parts if p)


def _assign_algorithm_category(text: str) -> str:
  text_lower = text.lower()
  for category, keywords in ALGORITHM_CATEGORY_KEYWORDS.items():
    if any(keyword in text_lower for keyword in keywords):
      return category
  return "Uncategorized"


def _assign_input_type(text: str) -> str:
  text_lower = text.lower()
  for input_type, keywords in INPUT_TYPE_KEYWORDS.items():
    if any(keyword in text_lower for keyword in keywords):
      return input_type
  return "Mixed/Other"


def _extract_problem_tags(text: str) -> list[str]:
  text_lower = text.lower()
  tags: list[str] = []
  for tag, keywords in TAG_KEYWORDS.items():
    if any(keyword in text_lower for keyword in keywords):
      tags.append(tag)
  return tags if tags else ["uncategorized"]


def _infer_output_type(cases: Sequence[dict]) -> str:
  for case in cases:
    expected = case.get("expected_output") if isinstance(case, dict) else None
    if expected is None:
      continue
    for candidate_type, label in OUTPUT_TYPE_MAPPINGS:
      if isinstance(expected, candidate_type):
        return label
  return DEFAULT_NA_VALUE


def _flag_negative_one(text: str, cases: Sequence[dict]) -> bool:
  if "-1" in text:
    return True
  for case in cases:
    if isinstance(case, dict) and case.get("expected_output") == -1:
      return True
  return False


def count_description_templates(series: pd.Series) -> Dict[str, int]:
  """설명 텍스트에서 템플릿 패턴 빈도 계산 (Aggregation 로직이지만 Scope 관련이라 여기에 위치 가능)"""
  counts: Dict[str, int] = {name: 0 for name in DESCRIPTION_TEMPLATE_PATTERNS}
  for value in series.fillna(""):
    for name, pattern in DESCRIPTION_TEMPLATE_PATTERNS.items():
      if pattern.search(str(value)):
        counts[name] += 1
  return counts


def enrich_dataframe(df: pd.DataFrame) -> pd.DataFrame:
  """원본 데이터프레임에 분석용 파생 변수(Features)를 추가합니다."""
  logger.info("Starting DataFrame enrichment and feature engineering.")
  enriched = df.copy()

  # 1. 기본 정규화
  enriched["difficulty_level"] = _normalize_difficulty(enriched.get("difficulty_level", pd.Series(dtype=str)))
  enriched["title"] = enriched.get("Title", enriched.get("title", "")).fillna("")
  enriched["description"] = enriched.get("Description", enriched.get("description", "")).fillna("")
  enriched["description_length"] = _safe_length(enriched["description"])

  # 2. 파싱
  enriched["examples_parsed"] = enriched.get("Examples", enriched.get("examples", pd.Series(dtype=object))).apply(_load_json_array)
  enriched["test_cases_parsed"] = enriched.get("Test Cases", enriched.get("test_cases", pd.Series(dtype=object))).apply(_load_json_array)
  enriched["constraints_parsed"] = enriched.get("Constraints", enriched.get("constraints", pd.Series(dtype=object))).apply(_load_json_array)

  # 3. 카운트
  enriched["num_examples"] = enriched["examples_parsed"].apply(len)
  enriched["num_test_cases"] = enriched["test_cases_parsed"].apply(len)
  enriched["constraints_count"] = enriched["constraints_parsed"].apply(len)

  # 4. 텍스트 분석 및 분류 (Scopes 설정)
  enriched["combined_text"] = enriched.apply(_collect_text, axis=1)
  enriched["algorithm_category"] = enriched["combined_text"].apply(_assign_algorithm_category)
  enriched["input_type"] = enriched["combined_text"].apply(_assign_input_type)
  enriched["problem_tags"] = enriched["combined_text"].apply(_extract_problem_tags)
  enriched["output_type"] = enriched["test_cases_parsed"].apply(_infer_output_type)

  enriched["returns_negative_one"] = enriched.apply(
    lambda row: _flag_negative_one(str(row.get("combined_text", "")), row.get("test_cases_parsed", [])),
    axis=1,
  )

  # 5. 시간 정보
  created = pd.to_datetime(enriched.get("CreatedAt", enriched.get("created_at")), errors="coerce")
  enriched["created_date"] = created.dt.date

  logger.info("DataFrame enrichment complete.")
  return enriched
