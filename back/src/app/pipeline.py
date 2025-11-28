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
from constants.messages import (
  PIPELINE_VERSION,
  PIPELINE_TITLE_START,
  PIPELINE_TITLE_COMPLETE,
  PIPELINE_TITLE_FINISHED,
  PIPELINE_MESSAGE_FATAL_EMPTY_DATA,
  PIPELINE_STEP_ENSURE_DIRS,
  PIPELINE_STEP_LOADING_DATA,
  PIPELINE_STEP_COMPUTE_STATS,
  PIPELINE_STEP_GENERATE_CHARTS,
  PIPELINE_STEP_SAVE_ARTIFACTS,
  PIPELINE_STEP_WRITE_JSON,
  PIPELINE_LOG_SAVED,
)


class DataAnalysisPipeline:
  # 애플리케이션 계층의 데이터 분석 파이프라인 유즈케이스.
  # 인프라/프리젠테이션 레이어의 구현(DataLoader, Visualizer, ArtifactWriter, ExcelReporter)을
  #  주입 받아 orchestration만 담당한다.

  def __init__(
          self,
          logger,
          data_loader: DataLoader,
          visualizer: Visualizer,
          artifact_writer: ArtifactWriter,
          reporter: ExcelReporter,
  ) -> None:
    self.logger = logger
    self.data_loader = data_loader
    self.visualizer = visualizer
    self.artifact_writer = artifact_writer
    self.reporter = reporter

  def run(self, options: PipelineOptions) -> None:
    steps = StepLogger(logger_name=self.logger.name)
    self._log_start_banner()

    self._prepare_infrastructure(steps)
    question_data = self._load_data(steps, options)

    if question_data is None or question_data.df.empty:
      self.logger.error(PIPELINE_MESSAGE_FATAL_EMPTY_DATA)
      return

    summary = self._compute_summary(steps, question_data)

    if options.generate_charts:
      self._generate_charts(steps, summary)

    excel_path = self._write_artifacts(steps, summary)

    self._log_completion(excel_path)

  # ====================================================
  # private helper methods
  # ====================================================

  def _log_start_banner(self) -> None:
    log_banner(
      PIPELINE_TITLE_START.format(version=PIPELINE_VERSION),
      color=FG.CYAN,
      line_color=FG.BLUE,
    )

  def _prepare_infrastructure(self, steps: StepLogger) -> None:
    steps.step(PIPELINE_STEP_ENSURE_DIRS)
    ensure_directories()

  def _load_data(self, steps: StepLogger, options: PipelineOptions) -> QuestionData:
    steps.step(PIPELINE_STEP_LOADING_DATA.format(path=options.data_file))
    return self.data_loader.load_csv_data(options.data_file)

  def _compute_summary(self, steps: StepLogger, question_data: QuestionData) -> DatasetSummary:
    steps.step(PIPELINE_STEP_COMPUTE_STATS)
    return compute_statistics(question_data.df)

  def _generate_charts(self, steps: StepLogger, summary: DatasetSummary) -> None:
    steps.step(PIPELINE_STEP_GENERATE_CHARTS)
    self.visualizer.create_and_save_charts(summary)

  def _write_artifacts(self, steps: StepLogger, summary: DatasetSummary) -> str:
    # JSON(3곳) + Excel 저장을 처리하고, Excel 경로를 반환한다.
    steps.step(PIPELINE_STEP_SAVE_ARTIFACTS)

    # JSON
    steps.step(PIPELINE_STEP_WRITE_JSON.format(target=OUTPUT_BACK_DIR.name))
    self.artifact_writer.write_analysis_json(summary, OUTPUT_BACK_DIR)
    self.artifact_writer.write_analysis_json(summary, FRONTEND_PUBLIC_SUMMARY_DIR)
    self.artifact_writer.write_analysis_json(summary, FRONTEND_SHARED_SUMMARY_DIR)

    # Excel
    def excel_progress_callback(current, total, message):
      steps.progress(current, total, message, channel="Excel")

    excel_path = self.reporter.write_report(summary, progress_callback=excel_progress_callback)
    return excel_path

  def _log_completion(self, excel_path: str) -> None:
    log_banner(
      PIPELINE_TITLE_COMPLETE,
      color=FG.GREEN,
      line_color=FG.GREEN,
    )

    self.logger.info(
      PIPELINE_LOG_SAVED.format(label="Public JSON", path=FRONTEND_PUBLIC_SUMMARY_DIR)
    )
    self.logger.info(
      PIPELINE_LOG_SAVED.format(label="Shared JSON", path=FRONTEND_SHARED_SUMMARY_DIR)
    )
    self.logger.info(
      PIPELINE_LOG_SAVED.format(label="Backend JSON", path=OUTPUT_BACK_DIR)
    )
    self.logger.info(
      PIPELINE_LOG_SAVED.format(label="Excel Report", path=excel_path)
    )

    log_banner(PIPELINE_TITLE_FINISHED, color=FG.YELLOW, line_color=FG.YELLOW)
