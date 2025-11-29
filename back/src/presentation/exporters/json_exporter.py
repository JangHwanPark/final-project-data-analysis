from __future__ import annotations
import json
from pathlib import Path
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
          filename: str = "summary.json"
  ) -> Optional[Path]:
    """
    데이터를 JSON으로 내보냅니다. (구 write_analysis_json)

    :param summary: 저장할 데이터 (DatasetSummary 객체 또는 dict)
    :param target_path: 저장할 디렉토리 경로 또는 파일 전체 경로
    :param filename: target_path가 디렉토리일 경우 사용할 기본 파일명
    """
    # 저장할 전체 경로 계산
    final_path = self._resolve_path(target_path, filename)

    # 데이터 직렬화 준비 (도메인 객체 -> dict)
    data_to_write = self._prepare_data(summary)

    # 실제 파일 쓰기
    return self._write_to_file(data_to_write, final_path)

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

    except Exception:
      logger.exception(f"ERROR: Failed to export JSON to {filepath}")
      return None
