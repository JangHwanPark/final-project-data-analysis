from __future__ import annotations

import json
from pathlib import Path
from typing import Optional, Any

from app_types.pipelien import AnalysisScope
from domain.entities.data_model import DatasetSummary
from infrastructure.logging import get_logger

logger = get_logger(__name__)


# =================================================================
# 분석 결과(DatasetSummary)를 JSON 파일로 내보내는 클래스
# =================================================================
class JsonExporter:
  def __init__(self):
    logger.info("JsonExporter initialized.")

  def export(
          self,
          summary: DatasetSummary | dict,
          target_path: Path,
          filename: str = "summary.json",
          scope: AnalysisScope = AnalysisScope.FULL
  ) -> Optional[Path]:
    """
    데이터를 JSON으로 내보냅니다. (구 write_analysis_json)

    :param summary: 저장할 데이터 (DatasetSummary 객체 또는 dict)
    :param target_path: 저장할 디렉토리 경로 또는 파일 전체 경로
    :param filename: target_path가 디렉토리일 경우 사용할 기본 파일명
    :param scope: 데이터 저장 범위 (FULL: 전체, BASIC: 요약, CUSTOM: 커스텀). 기본값은 FULL.
    """
    # 저장할 전체 경로 계산
    # final_path = self._resolve_path(target_path, filename)
    # 데이터 직렬화 준비 (도메인 객체 -> dict)
    # full_data = self._prepare_data(summary)
    # 스코프에 따른 데이터 필터링 수행
    # data_to_write = self._filter_data(full_data, scope)
    # DatasetSummary 객체를 딕셔너리로 변환
    data = summary.to_dict()
    # 전체 경로 생성
    filepath = target_path / filename
    logger.info(f"Attempting to write full summary to: {filepath}")
    return self._write_to_file(data, filepath)

  # ====================================================
  # 부분 저장용 메서드 (Config에 정의된 키만 뽑아서 저장)
  # DatasetSummary에서 특정 키(metrics, overview)만 추출하여 JSON으로 저장
  # ====================================================
  def export_subset(
          self,
          summary: DatasetSummary,
          target_dir: Path,
          filename: str,
          keys: list[str]
  ) -> Optional[Path]:
    # 저장할 경로 계산
    final_path = target_dir / filename

    # 필요한 데이터만 뽑아내기 (Filtering)
    subset_data = self._extract_subset_data(summary, keys)

    # 파일 쓰기 (기존 메서드 재사용)
    return self._write_to_file(subset_data, final_path)

  # 필터링 헬퍼 메서드
  def _filter_data(self, data: dict, scope: AnalysisScope) -> dict:
    # Full이면 필터링 없이 원본 반환
    if scope == AnalysisScope.FULL:
      return data

    # 데이터 구조 안전장치
    metrics = data.get("metrics", {})

    # === Basic Scope: 핵심 요약 정보만 남김 ===
    if scope == AnalysisScope.BASIC:
      return {
        "summary_info": data.get("summary_info", {}),
        "metrics": {
          # 꼭 필요한 것만 화이트리스트로 나열
          "difficulty_distribution": metrics.get("difficulty_distribution"),
          "problems_per_day": metrics.get("problems_per_day"),
          "total_questions": metrics.get("total_questions", 0),
          # 필요 없는 무거운 데이터(텍스트 분석, 복잡한 매트릭스 등)는 제외
        }
      }

    # === Custom Scope: 필요한 경우 정의 ===
    if scope == AnalysisScope.CUSTOM:
      return {
        "summary_info": data.get("summary_info", {}),
        "metrics": {
          "top_tags_distribution": metrics.get("top_tags_distribution"),
          # ... 원하는 것만
        }
      }

    return data  # 기본 Fallback

  # ====================================================
  # Private Helper Methods
  # 입력된 경로가 디렉토리인지 파일인지 판단하여 최종 경로 반환
  # ====================================================
  def _resolve_path(self, target_path: Path, default_filename: str) -> Path:
    # 확장자가 없으면 디렉토리로 간주하고 파일명 붙임
    if target_path.suffix == "":
      return target_path / default_filename
    return target_path

  # ====================================================
  # Private Helper Methods
  # 도메인 객체를 JSON 직렬화 가능한 dict로 변환
  # ====================================================
  def _prepare_data(self, summary: Any) -> dict:
    if hasattr(summary, "to_dict"):
      return summary.to_dict()
    if isinstance(summary, dict):
      return summary
    # Fallback: 문자열로 변환하여 감싸기
    return {"raw_data": str(summary)}

  # ====================================================
  # Private Helper Methods
  # 실제 파일 I/O 수행
  # ====================================================
  def _write_to_file(self, data: dict, filepath: Path) -> Optional[Path]:
    try:
      # 부모 디렉토리 생성
      filepath.parent.mkdir(parents=True, exist_ok=True)

      if filepath.is_dir():
        logger.error(f"ERROR: Target path is a directory, cannot write file: {filepath}")
        return None

      with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

      logger.info(f"SUCCESS: JSON exported to {filepath}")
      return filepath

    except Exception as e:
      logger.error(f"ERROR: Failed to export JSON to {filepath}.")
      logger.error(f"Error: {e}")
      return None

  # ====================================================
  # Private Helper: 데이터 필터링 로직
  # Config에 있는 키들을 Overview와 Metrics 양쪽에서 찾아서 하나의 metrics 객체로 통합
  # ====================================================
  def _extract_subset_data(self, summary: DatasetSummary, keys: list[str]) -> dict:
    # 전체 데이터를 딕셔너리로 변환
    full_data = self._prepare_data(summary)

    # 검색 대상(Search Pool) 병합
    # Config의 키가 'overview'에 있을 수도 있고 'metrics'에 있을 수도 있으므로
    # 검색하기 편하게 임시로 하나의 딕셔너리에 합칩니다.
    search_pool = {}

    # metrics 내용물 추가
    if "metrics" in full_data and isinstance(full_data["metrics"], dict):
      search_pool.update(full_data["metrics"])

    # overview 내용물 추가 (total_questions, days_span 등)
    if "overview" in full_data and isinstance(full_data["overview"], dict):
      search_pool.update(full_data["overview"])

    # 키 추출 (Extract)
    extracted_metrics = {}
    for key in keys:
      if key in search_pool:
        extracted_metrics[key] = search_pool[key]
      else:
        # (선택) 없는 키는 무시하거나, 로그를 남길 수 있습니다.
        pass

    # 최종 구조 반환 (프론트엔드 포맷: summary_info + metrics)
    return {
      "summary_info": {
        # 날짜 등 메타 정보는 full_data에 있는 timestamp(또는 generated_at)를 사용
        "generated_at": full_data.get("timestamp") or full_data.get("generated_at", ""),
        # 필요하다면 total_records 등을 추가
      },
      "metrics": extracted_metrics
    }
