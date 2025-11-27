from infrastructure.config import (
  ensure_directories,
  OUTPUT_BACK_DIR,
  FRONTEND_PUBLIC_SUMMARY_DIR,
  FRONTEND_SHARED_SUMMARY_DIR,
)
from infrastructure.data_loader import DataLoader
from infrastructure.artifact_writer import ArtifactWriter
from infrastructure.logging import StepLogger, log_banner
from infrastructure.logging.style import FG
from domain.service.metrics import compute_statistics
from domain.entities.data_model import QuestionData, DatasetSummary
from presentation.visualizer import Visualizer
from presentation.reports.excel_reporter import ExcelReporter
from .options import PipelineOptions


class DataAnalysisPipeline:
  def __init__(self, logger):
    self.logger = logger

  def run(self, options: PipelineOptions) -> None:
    steps = StepLogger(logger_name=self.logger.name)

    log_banner(
      "PYTHON DATA ANALYSIS PIPELINE STARTED (Ver 3.0)",
      color=FG.CYAN,
      line_color=FG.BLUE,
    )

    # [인프라 준비] 디렉토리 준비
    steps.step("Ensuring artifact directories...")
    ensure_directories()

    # [데이터 로드] Infrastructure Layer
    steps.step(f"Loading data from: {options.data_file}")
    data_loader = DataLoader()
    question_data: QuestionData = data_loader.load_csv_data(options.data_file)

    if question_data is None or question_data.df.empty:
      self.logger.error("FATAL: Data loading failed or resulted in empty DataFrame. Exiting pipeline.")
      return

    # [Compute statistics] 통계 계산
    steps.step("Computing domain metrics and statistics...")
    summary: DatasetSummary = compute_statistics(question_data.df)

    # [Presentation Layer] 시각화(차트)
    if options.generate_charts:
      steps.step("Generating charts and visualizations...")
      visualizer = Visualizer()
      visualizer.create_and_save_charts(summary)

    # JSON + Excel
    artifact_writer = ArtifactWriter()
    reporter = ExcelReporter()
    steps.step("Saving final artifacts across environments...")

    # JSON
    steps.step(f"Writing primary JSON artifact to {OUTPUT_BACK_DIR.name}.....")
    # [JSON 저장] 백엔드 아티팩트용 - 기록
    artifact_writer.write_analysis_json(summary, OUTPUT_BACK_DIR)
    # [JSON 저장] 프론트엔드 Public 디렉토리용
    artifact_writer.write_analysis_json(summary, FRONTEND_PUBLIC_SUMMARY_DIR)
    # [JSON 저장] 프론트엔드 Shared Data 디렉토리용
    artifact_writer.write_analysis_json(summary, FRONTEND_SHARED_SUMMARY_DIR)

    # [Excel 보고서 저장] 상세 데이터용(Excel progress 콜백)
    def excel_progress_callback(current, total, message):
      steps.progress(current, total, message, channel="Excel")

    excel_path = reporter.write_report(summary, progress_callback=excel_progress_callback)

    log_banner(
      "PIPELINE EXECUTION COMPLETE (Artifacts Summary)",
      color=FG.GREEN,
      line_color=FG.GREEN,
    )
    self.logger.info(f" Public JSON saved to: {FRONTEND_PUBLIC_SUMMARY_DIR}")
    self.logger.info(f" Shared JSON saved to: {FRONTEND_SHARED_SUMMARY_DIR}")
    self.logger.info(f" Excel Report saved to: {excel_path}")

    log_banner("PIPELINE FINISHED", color=FG.YELLOW, line_color=FG.YELLOW)
