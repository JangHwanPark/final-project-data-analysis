from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Optional, Callable, Union, Dict, Any
import time

# Infrastructure Dependencies
from infrastructure.logging import get_logger
from infrastructure.config import SUMMARIES_DIR

# Domain Dependencies
from domain.entities.data_model import DatasetSummary

logger = get_logger(__name__)


class ExcelReporter:
  # 분석 결과(DatasetSummary)를 상세 통계 테이블 형태의 Excel 파일로 저장하는 클래스.

  def __init__(self):
    logger.info("ExcelReporter initialized.")
    self.base_path = SUMMARIES_DIR  # 엑셀 파일도 JSON과 같은 디렉토리에 저장

  def write_report(
          self,
          summary: DatasetSummary,
          filename: str = "analysis_report.xlsx",
          progress_callback: Optional[Callable[[int, int, str], None]] = None
  ) -> Optional[Path]:
    """
    DatasetSummary 객체에서 주요 통계를 추출하여 다중 시트 Excel 파일로 저장합니다.

    :param summary: 저장할 DatasetSummary 도메인 객체.
    :param filename: 저장할 파일 이름.
    :param progress_callback: 진행 상태 업데이트를 위한 콜백 함수 (current, total, message).
    :return: 저장된 파일의 Path 객체 또는 실패 시 None.
    """
    filepath = self.base_path / filename
    logger.info(f"Attempting to write Excel report to {filepath}")

    # DatasetSummary에서 필요한 데이터 추출
    # metrics = summary.metrics
    if isinstance(summary, dict):
      # 딕셔너리일 경우, 'metrics' 키로 접근
      summary_dic = summary.get('overview', {})
      logger.warning("WARN: ExcelReporter received a 'dict' instead of a 'DatasetSummary' DTO.")
    else:
      # DatasetSummary 객체인 경우, 속성으로 접근
      try:
        summary_dic = summary.overview.to_dict()
      except AttributeError:
        logger.warning("WARN: summary.overview is not an object; attempting dict access.")
        return None

    # dic 에서 데이터 추출
    metrics = summary_dic.get('metrics', {})
    overview_data = summary_dic.get('overview', {})

    # 전체 시트 개수 정의 (총 5개)
    total_sheets = 5
    current_sheet = 0

    try:
      # pandas.ExcelWriter를 사용하여 다중 시트 작성 시작
      with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # 개요 시트 (Overview)
        sheet_name = '01_Overview'
        current_sheet += 1
        if progress_callback: progress_callback(current_sheet, total_sheets, f"Writing {sheet_name}")
        # 시뮬레이션 딜레이
        time.sleep(0.05)

        # overview_data 변수 사용 (이 시점에서는 반드시 dict이어야 함)
        df_overview = pd.DataFrame(
          list(overview_data.items()),
          columns=['Metric', 'Value']
        )
        df_overview.to_excel(writer, sheet_name=sheet_name, index=False)

        # 난이도 분포 (Difficulty Distribution)
        sheet_name = '02_Difficulty_Dist'
        current_sheet += 1
        if progress_callback: progress_callback(current_sheet, total_sheets, f"Writing {sheet_name}")
        time.sleep(0.05)
        # metrics['difficulty_distribution']이 유효한지 확인
        if 'difficulty_distribution' in metrics:
          df_difficulty = pd.DataFrame(metrics['difficulty_distribution'])
          df_difficulty.to_excel(writer, sheet_name=sheet_name, index=True)

        # 상위 태그 (Top Tags)
        sheet_name = '03_Top_Tags'
        current_sheet += 1
        if progress_callback: progress_callback(current_sheet, total_sheets, f"Writing {sheet_name}")
        time.sleep(0.05)
        if 'top_tags_distribution' in metrics:
          df_tags = pd.Series(metrics['top_tags_distribution']).to_frame(name='Count')
          df_tags.to_excel(writer, sheet_name=sheet_name, index=True)

        # 난이도별 평균 (Averages by Difficulty)
        sheet_name = '04_Difficulty_Averages'
        current_sheet += 1
        if progress_callback: progress_callback(current_sheet, total_sheets, f"Writing {sheet_name}")
        time.sleep(0.05)
        if 'avg_description_length_by_difficulty' in metrics and 'avg_test_cases_by_difficulty' in metrics:
          df_avg_desc = pd.Series(metrics['avg_description_length_by_difficulty']).to_frame(name='Avg_Desc_Length')
          df_avg_tests = pd.Series(metrics['avg_test_cases_by_difficulty']).to_frame(name='Avg_Test_Cases')
          df_averages = pd.concat([df_avg_desc, df_avg_tests], axis=1)
          df_averages.to_excel(writer, sheet_name=sheet_name, index=True)

        # 난이도-알고리즘 교차표 (Difficulty-Algorithm Matrix)
        sheet_name = '05_Difficulty_Algorithm'
        current_sheet += 1
        if progress_callback: progress_callback(current_sheet, total_sheets, f"Writing {sheet_name}")
        time.sleep(0.05)
        if 'difficulty_algorithm_matrix' in metrics:
          df_matrix = pd.DataFrame(metrics['difficulty_algorithm_matrix']).T
          df_matrix.to_excel(writer, sheet_name=sheet_name, index=True)

      logger.info(f"SUCCESS: Excel report written to {filepath}")
      return filepath

    except Exception as e:
      logger.exception(f"ERROR: Could not write Excel report to {filepath}.")
      return None
