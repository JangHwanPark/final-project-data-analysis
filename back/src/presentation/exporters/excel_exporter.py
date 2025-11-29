from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Optional, Callable, Dict, Any
import time

# Infrastructure Dependencies
from infrastructure.logging import get_logger

# Domain Dependencies
from domain.entities.data_model import DatasetSummary

logger = get_logger(__name__)


# ====================================================
# DatasetSummary를 엑셀 리포트 파일로 내보내는 클래스.
# ====================================================
class ExcelExporter:
  def __init__(self):
    logger.info("ExcelExporter initialized.")

  def export(
          self,
          summary: DatasetSummary,
          filepath: Path,
          progress_callback: Optional[Callable[[int, int, str], None]] = None
  ) -> Optional[Path]:
    """
    분석 결과를 엑셀 파일로 내보냅니다.

    :param summary: 도메인 데이터 객체 (DatasetSummary)
    :param filepath: 저장할 엑셀 파일의 전체 경로 (파일명 포함)
    :param progress_callback: 진행률 업데이트 콜백 함수
    :return: 저장 성공 시 경로, 실패 시 None
    """
    logger.info(f"Attempting to export Excel report to {filepath}")

    # 데이터 추출 (Helper 함수 사용)
    data_context = self._extract_data_context(summary)
    if not data_context:
      return None

    # 시트 작업 정의
    tasks = [
      ("01_Overview", self._write_overview),
      ("02_Difficulty_Dist", self._write_difficulty_dist),
      ("03_Top_Tags", self._write_top_tags),
      ("04_Difficulty_Averages", self._write_averages),
      ("05_Difficulty_Algorithm", self._write_matrix),
    ]

    total_sheets = len(tasks)

    try:
      # 상위 디렉토리 생성
      filepath.parent.mkdir(parents=True, exist_ok=True)

      with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        for idx, (sheet_name, writer_func) in enumerate(tasks, 1):
          # Progress Logging
          if progress_callback:
            progress_callback(idx, total_sheets, f"Writing {sheet_name}")

          # 실제 시트 작성 실행
          writer_func(writer, sheet_name, data_context)

          # 시각적 딜레이 (UI용, 필요 없으면 제거 가능)
          time.sleep(0.05)

      logger.info(f"SUCCESS: Excel report exported to {filepath}")
      return filepath

    except Exception as e:
      logger.exception(f"ERROR: Could not export Excel report to {filepath}.")
      return None

  # ====================================================
  # Private Helper Methods (Data Extraction & Writing)
  # DatasetSummary 객체에서 엑셀 생성에 필요한 raw dict 데이터를 추출
  # ====================================================
  def _extract_data_context(self, summary: DatasetSummary | dict) -> Optional[Dict[str, Any]]:
    try:
      if hasattr(summary, "to_dict"):
        full_data = summary.to_dict()
      elif isinstance(summary, dict):
        full_data = summary
      else:
        logger.error(f"Invalid summary type: {type(summary)}")
        return None

      # 구조에 맞춰 데이터 분리 (metrics, overview 키가 있다고 가정)
      return {
        "overview": full_data.get("overview", {}),
        "metrics": full_data.get("metrics", {})
      }
    except Exception as e:
      logger.exception("Failed to extract data context from summary.")
      return None

  # ====================================================
  # [시트 1] Overview 작성
  # 전체 문제 수, 난이도 개수, 데이터 수집 기간 등 데이터셋의 전반적인 요약 정보를 기록
  # Key-Value 형태의 2열 테이블로 저장됨
  # ====================================================
  def _write_overview(self, writer: pd.ExcelWriter, sheet_name: str, context: dict):
    overview_data = context["overview"]
    df = pd.DataFrame(list(overview_data.items()), columns=['Metric', 'Value'])
    df.to_excel(writer, sheet_name=sheet_name, index=False)

  # ====================================================
  # [시트 2] Difficulty Distribution 작성
  # 난이도별 문제 개수(counts)와 비율(percentages)을 기록
  # metrics['difficulty_distribution'] 데이터를 사용
  # ====================================================
  def _write_difficulty_dist(self, writer: pd.ExcelWriter, sheet_name: str, context: dict):
    data = context["metrics"].get('difficulty_distribution')
    if data:
      pd.DataFrame(data).to_excel(writer, sheet_name=sheet_name, index=True)

  # ====================================================
  # [시트 3] Top Tags 작성
  # 가장 많이 등장한 상위 태그들의 빈도수를 기록
  # metrics['top_tags_distribution'] 데이터를 사용
  # ====================================================
  def _write_top_tags(self, writer: pd.ExcelWriter, sheet_name: str, context: dict):
    data = context["metrics"].get('top_tags_distribution')
    if data:
      pd.Series(data).to_frame(name='Count').to_excel(writer, sheet_name=sheet_name, index=True)

  # ====================================================
  # [시트 4] Difficulty Averages 작성
  # 난이도별 평균 설명 길이(Avg_Desc_Length)와
  # 평균 테스트 케이스 수(Avg_Test_Cases)를 하나의 테이블로 병합하여 기록
  # ====================================================
  def _write_averages(self, writer: pd.ExcelWriter, sheet_name: str, context: dict):
    metrics = context["metrics"]
    avg_desc = metrics.get('avg_description_length_by_difficulty')
    avg_test = metrics.get('avg_test_cases_by_difficulty')

    if avg_desc and avg_test:
      df_desc = pd.Series(avg_desc).to_frame(name='Avg_Desc_Length')
      df_test = pd.Series(avg_test).to_frame(name='Avg_Test_Cases')
      pd.concat([df_desc, df_test], axis=1).to_excel(writer, sheet_name=sheet_name, index=True)

  # ====================================================
  # [시트 5] Difficulty Algorithm Matrix 작성
  # 난이도(행)와 알고리즘 카테고리(열) 간의 교차 분석표(Cross-tabulation)를 기록
  # 보기 좋게 하기 위해 행/열을 전치(Transpose, .T)하여 저장
  # ====================================================
  def _write_matrix(self, writer: pd.ExcelWriter, sheet_name: str, context: dict):
    data = context["metrics"].get('difficulty_algorithm_matrix')
    if data:
      pd.DataFrame(data).T.to_excel(writer, sheet_name=sheet_name, index=True)
