from __future__ import annotations
from infrastructure.runtime.venv import ensure_venv
ensure_venv(module_to_run="app.main_interactive")

from app.interactive import ask_user_for_options
from app.pipeline import DataAnalysisPipeline
from infrastructure.logging import get_logger
from infrastructure.logging import log_banner
from infrastructure.logging.style import FG

# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == "__main__":
  log_banner(
    "PYTHON DATA ANALYSIS PIPELINE STARTED (Ver 3.0)",
    color=FG.CYAN,
    line_color=FG.BLUE,
  )

  options = ask_user_for_options()
  DataAnalysisPipeline(logger=get_logger("interactive")).run(options)