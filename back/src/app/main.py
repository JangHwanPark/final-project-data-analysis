from __future__ import annotations

import argparse
from pathlib import Path
import sys
import os

# =================================================================
# 중요: 실행 안내
# 이 파일을 실행하려면 반드시 패키지 루트(backend/)에서
# 'python -m src.app.main' 명령어를 사용해야 합니다.
# (스크립트로 직접 실행 시 ModuleNotFoundError 발생)
# =================================================================

# =================================================================
# 중요: 실행 경로 설정 (스크립트 직접 실행을 위한 방어 로직)
# 'python src/app/main.py' 형태로 실행 시 'src' 패키지를 인식하게 합니다.
# =================================================================
try:
    # 현재 파일의 부모 디렉토리(src/app)에서 두 단계 위 (backend/)를 프로젝트 루트로 설정
    PROJECT_ROOT_DIR = Path(__file__).resolve().parents[2]
    if str(PROJECT_ROOT_DIR) not in sys.path:
        sys.path.append(str(PROJECT_ROOT_DIR))
except Exception:
    # 예외 발생 시 로깅 대신 단순 경고 처리
    pass
# =================================================================

# --- Infrastructure Layer 임포트 ---
from infrastructure.config import ensure_directories, DATA_FILE, SUMMARIES_DIR
from infrastructure.data_loader import DataLoader
from infrastructure.artifact_writer import ArtifactWriter
from infrastructure.logging import get_logger, StepLogger

# --- Domain Layer 임포트 ---
from domain.service.metrics import compute_statistics
from domain.entities.data_model import QuestionData, DatasetSummary

logger = get_logger("__name__")


def parse_arguments() -> Path:
  # 명령줄 인자를 파싱하고 분석할 데이터 파일 경로를 반환
  parser = argparse.ArgumentParser(
    description="Python 데이터 분석 파이프라인 실행기.",
    epilog=f"기본 CSV 파일 경로: {DATA_FILE}"
  )
  parser.add_argument(
    "--data-file",
    type=Path,
    default=DATA_FILE,
    help="분석할 CSV 파일의 경로를 지정합니다."
  )
  args = parser.parse_args()
  return args.data_file


def _get_data_loader() -> DataLoader:
  # DataLoader 인스턴스를 생성하여 반환
  # DataLoader는 현재 config에 따라 동작하므로 인수를 전달할 필요가 없습니다.
  return DataLoader()


def _get_artifact_writer() -> ArtifactWriter:
  # ArtifactWriter 인스턴스를 생성하여 반환
  # ArtifactWriter도 현재 config에 따라 작동하므로 인수를 전달할 필요가 없습니다.
  return ArtifactWriter()


def run_pipeline():
  logger.info("==============================================")
  logger.info(" PYTHON DATA ANALYSIS PIPELINE STARTED (Ver 2.0)")
  logger.info("==============================================")

  # 명령줄 인자 파싱
  input_file_path = parse_arguments()
  # 총 4단계: 디렉토리 준비, 로드, 분석, 저장
  steps = StepLogger(total_steps=4, logger_name=logger.name)

  try:
    # [인프라 준비] artifacts 디렉토리 준비
    steps.step("Ensuring directories...")
    ensure_directories()

    # [데이터 로드] Infrastructure Layer
    steps.step(f"Loading data from: {input_file_path}")

    # 헬퍼 함수를 사용하여 인스턴스 생성
    data_loader = _get_data_loader()
    question_data: QuestionData = data_loader.load_csv_data(input_file_path)

    if question_data is None or question_data.df.empty:
      logger.error("FATAL: Data loading failed or resulted in empty DataFrame. Exiting pipeline.")
      return

    # [통계 계산] Compute statistics
    steps.step("Computing domain metrics and statistics...")
    summary: DatasetSummary = compute_statistics(question_data.df)

    # 저장 경로 설정 & JSON 파일로 저장(Export as JSON file)
    # output_path = SUMMARIES_DIR / "summary.json"
    # steps.step(f"Writing final summary DTO to {output_path}")

    # [아티팩트 저장] Infrastructure Layer
    output_path = SUMMARIES_DIR / "summary.json"
    steps.step(f"Writing final summary DTO to {output_path}")

    # 헬퍼 함수를 사용하여 인스턴스 생성
    artifact_writer = _get_artifact_writer()
    json_path = artifact_writer.write_analysis_json(summary, output_path)

    logger.info("\n==============================================")
    logger.info(" PIPELINE EXECUTION COMPLETE.")
    logger.info(f" Summary JSON saved to: {json_path}")
    logger.info("==============================================")

  except Exception as e:
    logger.exception("Pipeline failed due to an unexpected error.")
    logger.error("Pipeline failed.")
  finally:
    logger.info("=== Pipeline Finished ===")

# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
  run_pipeline()
