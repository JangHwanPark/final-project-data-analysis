from pathlib import Path
from infrastructure.config import DATA_FILE

CLI_DESCRIPTION = "Python 데이터 분석 파이프라인 실행기."
CLI_EPILOG = f"기본 CSV 파일 경로: {DATA_FILE}"

ENGINE_DEFAULT = "csv"
ENGINE_CHOICES = ["csv", "json", "db"]

DEFAULT_DATA_FILE: Path = DATA_FILE
