from __future__ import annotations

import argparse
from pathlib import Path
from infrastructure.logging.style import FG

# =================================================================
# CLI entry point for the backend data analysis pipeline.
# =================================================================
# --- Infrastructure Layer 임포트 ---
from infrastructure.config import (
  ensure_directories,
  DATA_FILE,
  OUTPUT_BACK_DIR,
  FRONTEND_PUBLIC_SUMMARY_DIR,
  FRONTEND_SHARED_SUMMARY_DIR,
)
from infrastructure.data_loader import DataLoader
from infrastructure.artifact_writer import ArtifactWriter
from infrastructure.logging import get_logger, StepLogger, log_banner

# --- Domain Layer 임포트 ---
from domain.service.metrics import compute_statistics
from domain.entities.data_model import QuestionData, DatasetSummary

# --- Presentation Layer 임포트 ---
from presentation.visualizer import Visualizer
from presentation.reports.excel_reporter import ExcelReporter

# logger = get_logger("pipeline")
logger = get_logger(Path(__file__).stem)

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

def _get_visualizer() -> Visualizer:
    # Visualizer 인스턴스를 생성하여 반환
    return Visualizer()

def _get_excel_reporter() -> ExcelReporter:
    # ExcelReporter 인스턴스를 생성하여 반환
    return ExcelReporter()


def run_pipeline():
  # [Application Layer] 데이터 분석 파이프라인의 전체 실행 순서를 관리
  log_banner(
    "PYTHON DATA ANALYSIS PIPELINE STARTED (Ver 3.0)",
    color=FG.CYAN,
    line_color=FG.BLUE,
  )

  # 명령줄 인자 파싱
  input_file_path = parse_arguments()
  # steps = StepLogger(total_steps=5, logger_name=logger.name)
  steps = StepLogger(logger_name=logger.name)

  try:
    # [인프라 준비] artifacts 디렉토리 준비
    steps.step("Ensuring artifact directories...")
    ensure_directories()

    # [데이터 로드] Infrastructure Layer
    steps.step(f"Loading data from: {input_file_path}")

    # 헬퍼 함수를 사용하여 인스턴스 생성
    data_loader = _get_data_loader()
    question_data: QuestionData = data_loader.load_csv_data(input_file_path)

    if question_data is None or question_data.df.empty:
      logger.error("FATAL: Data loading failed or resulted in empty DataFrame. Exiting pipeline.")
      return

    # [Compute statistics] 통계 계산
    steps.step("Computing domain metrics and statistics...")
    summary: DatasetSummary = compute_statistics(question_data.df)

    # [Presentation Layer] 시각화
    steps.step("Generating charts and visualizations...")
    visualizer = _get_visualizer()
    visualizer.create_and_save_charts(summary)

    # [Infrastructure & Presentation Layer] 아티팩트 저장 및 보고서 생성
    artifact_writer = _get_artifact_writer()
    reporter = _get_excel_reporter()
    steps.step("Saving final artifacts across environments...")

    # [JSON 저장] 백엔드 아티팩트용 - 기록
    steps.step(f"Writing primary JSON artifact to {OUTPUT_BACK_DIR.name}.....")
    artifact_writer.write_analysis_json(summary, OUTPUT_BACK_DIR)

    # [JSON 저장] 프론트엔드 Public 디렉토리용
    steps.logger.info(f"Writing public JSON artifact to {FRONTEND_PUBLIC_SUMMARY_DIR.name}...")
    artifact_writer.write_analysis_json(summary, FRONTEND_PUBLIC_SUMMARY_DIR)

    # [JSON 저장] 프론트엔드 Shared Data 디렉토리용
    steps.logger.info(f"Writing public JSON artifact to {FRONTEND_SHARED_SUMMARY_DIR.name}...")
    artifact_writer.write_analysis_json(summary, FRONTEND_SHARED_SUMMARY_DIR)

    # [Excel 보고서 저장] 상세 데이터용
    def excel_progress_callback(current, total, message):
      # percentage = (current / total) * 100
      # steps.logger.info(f"   [-- Excel Sheet --] {percentage:.0f}%: {message}")
      steps.progress(current, total, message)

    steps.logger.info(" -> Generating detailed Excel Report (5 sheets) with progress simulation...")
    excel_path = reporter.write_report(summary, progress_callback=excel_progress_callback)

    log_banner(
      "PIPELINE EXECUTION COMPLETE (Artifacts Summary)",
      color=FG.GREEN,
      line_color=FG.GREEN,
    )
    logger.info(f" Public JSON saved to: {FRONTEND_PUBLIC_SUMMARY_DIR}")
    logger.info(f" Shared JSON saved to: {FRONTEND_SHARED_SUMMARY_DIR}")
    logger.info(f" Excel Report saved to: {excel_path}")

  except Exception as e:
    log_banner("PIPELINE FAILED", color=FG.RED, line_color=FG.RED)
    logger.exception("Pipeline failed due to an unexpected error.")
  finally:
    log_banner("PIPELINE FINISHED", color=FG.YELLOW, line_color=FG.YELLOW)

# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
  run_pipeline()
