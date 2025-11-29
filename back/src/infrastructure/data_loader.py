from __future__ import annotations
import pandas as pd
from pathlib import Path
from typing import Optional, Any

# Infrastructure Dependencies
from infrastructure.logging import get_logger
from config.default import ENCODING, DATE_COLUMNS

# Domain Dependencies
from domain.entities.data_model import QuestionData

logger = get_logger(__name__)


class DataLoader:
  # 데이터 로딩을 담당하는 인프라스트럭처 클래스.
  # CSV 파일을 읽어 pandas DataFrame을 QuestionData 도메인 객체로 반환합니다.

  def __init__(self):
    logger.info("DataLoader initialized.")

  def load_csv_data(self, filepath: Path) -> Optional[QuestionData]:
    """
    주어진 경로에서 CSV 파일을 로드합니다.

    :param filepath: 로드할 CSV 파일의 전체 경로 (Path 객체).
    :return: QuestionData 객체 또는 파일 로드 실패 시 None.
    """
    logger.info(f"Attempting to load data from {filepath}")

    if not filepath.exists():
      logger.error(f"ERROR: File not found at {filepath}")
      return None

    try:
      # 설정 파일의 인코딩과 날짜 컬럼을 사용하여 로드합니다.
      df = pd.read_csv(
        filepath,
        encoding=ENCODING,
        parse_dates=[col for col in DATE_COLUMNS if col in pd.read_csv(filepath, nrows=1).columns]  # 컬럼 존재 시에만 파싱 시도
      )

      # 최소 필수 컬럼 검증 (프로젝트 데이터에 맞게 수정)
      required_cols = ['title', 'description', 'difficulty_level']
      missing_cols = []
      logger.info("Starting required column validation:")
      for col in required_cols:
        if col in df.columns:
          logger.info(f" -> FOUND column: '{col}'")
        else:
          logger.warning(f" -> MISSING column: '{col}'")
          missing_cols.append(col)

      # 최종 경고 메시지 출력 (누락된 컬럼이 있을 경우)
      if missing_cols:
        logger.warning(f"WARN: Missing required columns in CSV: {missing_cols}")

      logger.info(f"SUCCESS: Data loaded. Total records: {len(df)}")
      return QuestionData(df=df, source_name=filepath.name)

    except pd.errors.EmptyDataError:
      logger.error(f"ERROR: CSV file is empty at {filepath}")
      return None
    except Exception as e:
      logger.exception(f"ERROR: An unexpected error occurred during data loading from {filepath}.")
      return None
