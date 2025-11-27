from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

# Infrastructure Dependencies
from infrastructure.logging import get_logger
from infrastructure.config import SUMMARIES_DIR

# Domain Dependencies
from domain.entities.data_model import DatasetSummary

logger = get_logger(__name__)


class ArtifactWriter:
  # 분석 결과(DatasetSummary)를 JSON 등
  # 구조화된 파일 형태로 저장하는 인프라스트럭처 클래스
  # 파일 I/O 관련 책임을 수행

  def __init__(self):
    logger.info("ArtifactWriter initialized.")

  def write_analysis_json(self, summary: DatasetSummary, filepath: Path) -> Optional[Path]:
    """
    DatasetSummary 객체를 JSON 파일로 직렬화하여 저장합니다.

    :param summary: 저장할 DatasetSummary 도메인 객체.
    :param filepath: 저장할 JSON 파일의 전체 경로 (Path 객체).
    :return: 저장된 파일의 Path 객체 또는 실패 시 None.
    """
    if filepath.parent != SUMMARIES_DIR:
      logger.warning(f"WARN: Writing to non-standard summaries directory: {filepath.parent}")

    # JSON 직렬화 가능한 딕셔너리로 변환
    if isinstance(summary, dict):
      data_to_write = dict(summary)
    else:
      data_to_write = summary.to_dict()

    timestamp = datetime.utcnow().isoformat()
    if "timestamp" in data_to_write:
      data_to_write["timestamp"] = timestamp
    else:
      data_to_write["generated_at"] = timestamp

    try:
      with open(filepath, 'w', encoding='utf-8') as f:
        # 가독성을 위해 indent=4로 설정
        json.dump(data_to_write, f, ensure_ascii=False, indent=4)
      logger.info(f"SUCCESS: Analysis JSON written to {filepath}")
      return filepath
    except IOError as e:
      logger.exception(f"ERROR: Could not write JSON file to {filepath}.")
      return None
    except Exception as e:
      logger.exception("ERROR: Unexpected error during JSON serialization.")
      return None
