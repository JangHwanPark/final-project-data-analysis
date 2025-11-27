from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Optional

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

  def write_report(self, summary: DatasetSummary, filename: str = "analysis_report.xlsx") -> Optional[Path]:
    """
    DatasetSummary 객체에서 주요 통계를 추출하여 다중 시트 Excel 파일로 저장합니다.

    :param summary: 저장할 DatasetSummary 도메인 객체.
    :param filename: 저장할 파일 이름.
    :return: 저장된 파일의 Path 객체 또는 실패 시 None.
    """
    filepath = self.base_path / filename
    logger.info(f"Attempting to write Excel report to {filepath}")

    # DatasetSummary에서 필요한 데이터 추출
    metrics = summary.metrics

    try:
      with pd.ExcelWriter(filepath, engine='openpyxl') as writer:

        # 개요 시트 (Overview)
        overview_data = summary.overview.to_dict()
        df_overview = pd.DataFrame(
          list(overview_data.items()),
          columns=['Metric', 'Value']
        )
        df_overview.to_excel(writer, sheet_name='01_Overview', index=False)

        # 난이도 분포 (Difficulty Distribution)
        df_difficulty = pd.DataFrame(metrics['difficulty_distribution'])
        df_difficulty.to_excel(writer, sheet_name='02_Difficulty_Dist', index=True)

        # 상위 태그 (Top Tags)
        df_tags = pd.Series(metrics['top_tags_distribution']).to_frame(name='Count')
        df_tags.to_excel(writer, sheet_name='03_Top_Tags', index=True)

        # 난이도별 평균 (Averages by Difficulty)
        df_avg_desc = pd.Series(metrics['avg_description_length_by_difficulty']).to_frame(name='Avg_Desc_Length')
        df_avg_tests = pd.Series(metrics['avg_test_cases_by_difficulty']).to_frame(name='Avg_Test_Cases')

        df_averages = pd.concat([df_avg_desc, df_avg_tests], axis=1)
        df_averages.to_excel(writer, sheet_name='04_Difficulty_Averages', index=True)

        # 난이도-알고리즘 교차표 (Difficulty-Algorithm Matrix)
        df_matrix = pd.DataFrame(metrics['difficulty_algorithm_matrix']).T
        df_matrix.to_excel(writer, sheet_name='05_Difficulty_Algorithm', index=True)

      logger.info(f"SUCCESS: Excel report written to {filepath}")
      return filepath

    except Exception as e:
      logger.exception(f"ERROR: Could not write Excel report to {filepath}.")
      return None
