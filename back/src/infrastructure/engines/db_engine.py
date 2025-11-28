from __future__ import annotations

from dataclasses import dataclass
import sqlite3
import pandas as pd
from .base import DataLoadEngine
from infrastructure.logging import get_logger, FG

logger = get_logger(__name__)


@dataclass
class DBConfig:
  # DB 엔진 확장용 설정(현재 구현되지 않음)
  db_path: str | None = None


class DBDataEngine(DataLoadEngine):
  # SQLite DB에서 쿼리를 실행하고 DataFrame으로 반환하는 엔진.
  """
  DBDataEngine (미구현)
  현재는 CSV 기반 파이프라인만 지원하며,
  향후 DB 기반 로딩이 필요할 때 확장 예정.
  """

  def __init__(self, config: DBConfig):
    self.config = config

  # ==========================================
  # 실제 파이프라인에서는 절대 호출되면 안되는 load
  # ==========================================
  def load(self, source: str) -> pd.DataFrame:
    logger.error("DBDataEngine.load() 호출됨 — 현재 구현되지 않았습니다.")
    raise NotImplementedError(
      "DBDataEngine은 아직 구현되지 않았습니다. "
      "CSV 또는 JSON 엔진만 사용할 수 있습니다."
    )

  # ==========================================
  # 실제 파이프라인에서는 절대 호출되면 안되는 load
  # ==========================================
  def none_load(self) -> pd.DataFrame:
    logger.error(
      "DBDataEngine.dev_load() 호출됨 — DB 엔진은 아직 구현되지 않았습니다.",
    )
    raise NotImplementedError(
      "DBDataEngine은 현재 구현되지 않았습니다. "
      "CSV 또는 JSON 엔진만 사용할 수 있습니다."
    )

  # ==========================================
  # 실제 파이프라인에서는 절대 호출되면 안되는 load
  # ==========================================
  def dev_load(self, source: str) -> pd.DataFrame:
    raise NotImplementedError(
      "DBDataEngine은 현재 구현되지 않았습니다. "
      "CSV 또는 JSON 엔진만 사용할 수 있습니다."
    )

  # ==========================================
  # 실제 파이프라인에서는 절대 호출되면 안되는 load
  # ==========================================
  def preview_load(self, source: str) -> pd.DataFrame:
    # source에는 SQL 쿼리 문자열이 온다고 가정.
    if not self.config.db_path:
      logger.error("preview_load 실패 — db_path 설정 없음")
      raise ValueError("preview_load 사용 시 db_path가 필요합니다.")

    query = source
    logger.warning(f"[PREVIEW] SQLite 쿼리 실행: {query}")
    conn = sqlite3.connect(self.config.db_path)

    try:
      df = pd.read_sql_query(query, conn)
      logger.info(f"[PREVIEW] {len(df)} rows 로드됨")
      return df
    finally:
      conn.close()
