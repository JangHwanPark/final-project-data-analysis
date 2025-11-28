from __future__ import annotations

from infrastructure.runtime.venv import ensure_venv

ensure_venv(module_to_run="app.main")

from pathlib import Path
from infrastructure.data_loader import DataLoader
from infrastructure.artifact_writer import ArtifactWriter
from presentation.visualizer import Visualizer
from presentation.reports.excel_reporter import ExcelReporter
from infrastructure.logging import get_logger, log_banner
from infrastructure.logging.style import FG
from app.pipeline import DataAnalysisPipeline
from app.interactive import ask_user_for_options
from app.cli import parse_arguments
from constants.messages import (
  PIPELINE_INTERACTIVE_ENABLED,
  PIPELINE_TITLE_FAILED,
  PIPELINE_ERROR_MESSAGE
)

logger = get_logger(Path(__file__).stem)


def run_pipeline():
  base_options, interactive = parse_arguments()
  pipeline = DataAnalysisPipeline(
    logger=logger,
    data_loader=DataLoader(),
    visualizer=Visualizer(),
    artifact_writer=ArtifactWriter(),
    reporter=ExcelReporter(),
  )

  if interactive:
    log_banner(PIPELINE_INTERACTIVE_ENABLED, color=FG.CYAN, line_color=FG.CYAN)
    options = ask_user_for_options()
  else:
    options = base_options

  try:
    pipeline.run(options)
  except Exception:
    log_banner(PIPELINE_TITLE_FAILED, color=FG.RED, line_color=FG.RED)
    logger.exception(PIPELINE_ERROR_MESSAGE)


if __name__ == "__main__":
  run_pipeline()
