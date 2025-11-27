from __future__ import annotations

import argparse
from pathlib import Path
from infrastructure.logging import get_logger, log_banner
from infrastructure.config import DATA_FILE
from infrastructure.logging.style import FG
from app.options import PipelineOptions
from app.pipeline import DataAnalysisPipeline

# logger = get_logger("pipeline")
logger = get_logger(Path(__file__).stem)


def parse_arguments() -> PipelineOptions:
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
  # 나중에 여기서 --no-charts, --no-excel, --interactive 이런 거도 추가 가능
  args = parser.parse_args()

  return PipelineOptions(
    data_file=args.data_file,
    generate_charts=True,
    generate_excel=True,
  )


# =================================================================
# CLI entry point for the backend data analysis pipeline.
# =================================================================
def run_pipeline():
  options = parse_arguments()
  pipeline = DataAnalysisPipeline(logger=logger)

  try:
    pipeline.run(options)
  except Exception:
    log_banner("PIPELINE FAILED", color=FG.RED, line_color=FG.RED)
    logger.exception("Pipeline failed due to an unexpected error.")


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
  run_pipeline()
