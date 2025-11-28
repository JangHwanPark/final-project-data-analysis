from __future__ import annotations
from infrastructure.runtime.venv import ensure_venv
ensure_venv(module_to_run="app.main")

import argparse
from pathlib import Path
from infrastructure.logging import get_logger, log_banner
from infrastructure.config import DATA_FILE
from infrastructure.logging.style import FG
from app.options import PipelineOptions
from app.pipeline import DataAnalysisPipeline
from app.interactive import ask_user_for_options

# logger = get_logger("pipeline")
logger = get_logger(Path(__file__).stem)


def parse_arguments() -> tuple[PipelineOptions, bool]:
  parser = argparse.ArgumentParser(
    description="Python 데이터 분석 파이프라인 실행기.",
    epilog=f"기본 CSV 파일 경로: {DATA_FILE}",
  )
  
  parser.add_argument(
    "--data-file",
    type=Path,
    default=DATA_FILE,
    help="분석할 CSV 파일의 경로를 지정합니다.",
  )

  parser.add_argument(
    "--engine",
    type=str,
    default="csv",
    choices=["csv", "json", "db"],
    help="데이터 로딩 엔진 선택(csv, json, db)"
  )

  parser.add_argument(
    "--interactive", "-i",
    action="store_true",
    help="인터랙티브 모드(questionary)로 실행합니다.",
  )

  # TODO: 나중에 해볼꺼
  # 나중에 여기서 --no-charts, --no-excel, --interactive 이런 거도 추가 가능
  args = parser.parse_args()

  options = PipelineOptions(
    data_file=args.data_file,
    generate_charts=True,
    generate_excel=True,
    engine=args.engine,
  )

  return options, args.interactive


# =================================================================
# CLI entry point for the backend data analysis pipeline.
# =================================================================
def run_pipeline():
  base_options, interactive = parse_arguments()
  pipeline = DataAnalysisPipeline(logger=logger)

  if interactive:
    log_banner("INTERACTIVE MODE ENABLED", color=FG.CYAN, line_color=FG.CYAN)
    options = ask_user_for_options()
  else:
    options = base_options

  try:
    pipeline.run(options)
  except Exception:
    log_banner("PIPELINE FAILED", color=FG.RED, line_color=FG.RED)
    logger.exception("Pipeline failed due to an unexpected error.")


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
  run_pipeline()
