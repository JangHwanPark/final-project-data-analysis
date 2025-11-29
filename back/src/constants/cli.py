from pathlib import Path
from constants.path import DataPaths

CLI_DESCRIPTION = "Python 데이터 분석 파이프라인 실행기."
CLI_EPILOG = f"기본 CSV 파일 경로: {DataPaths.QUESTIONS_FILE}"

ENGINE_DEFAULT = "csv"
ENGINE_CHOICES = ["csv", "json", "db"]

DEFAULT_DATA_FILE: Path = DataPaths.QUESTIONS_FILE
