from infrastructure.config import (
  ensure_directories,
  OUTPUT_BACK_DIR,
  FRONTEND_PUBLIC_SUMMARY_DIR,
  FRONTEND_SHARED_SUMMARY_DIR,
)
from infrastructure.data_loader import DataLoader
from infrastructure.logging import StepLogger, log_banner
from infrastructure.logging.style import FG
from domain.service.metrics import compute_statistics
from domain.entities.data_model import QuestionData, DatasetSummary
from presentation.exporters import JsonExporter, ExcelExporter, ChartExporter
from .pipeline_options import PipelineOptions
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
  PIPELINE_ENGINE_NOTE,
)


# ====================================================
# 애플리케이션 계층의 데이터 분석 파이프라인 유즈케이스.
# 인프라/프리젠테이션 레이어의 구현(DataLoader, Visualizer, ArtifactWriter, ExcelReporter)을
# 주입 받아 orchestration만 담당.
# ====================================================
class DataAnalysisPipeline:
  def __init__(
          self,
          logger,
          data_loader: DataLoader,
          chart_exporter: ChartExporter,
          json_exporter: JsonExporter,
          excel_exporter: ExcelExporter,
  ) -> None:
    self.logger = logger
    self.data_loader = data_loader
    self.chart_exporter = chart_exporter
    self.json_exporter = json_exporter
    self.excel_exporter = excel_exporter

  def run(self, options: PipelineOptions) -> None:
    steps = StepLogger(logger_name=self.logger.name)
    self._log_start_banner()

    self._prepare_infrastructure(steps)
    question_data = self._load_data(steps, options)

    if question_data is None or question_data.df.empty:
      self.logger.error(PIPELINE_MESSAGE_FATAL_EMPTY_DATA)
      return

    summary = self._compute_summary(steps, question_data)

    # [수정 4] options 객체를 helper 메서드에 전달 (경로 정보가 options에 있음)
    if options.generate_charts:
      self._generate_charts(steps, summary, options)

    excel_path = self._write_artifacts(steps, summary, options)

    self._log_completion(excel_path, options)

  # ====================================================
  # private helper methods
  # ====================================================
  def _log_start_banner(self) -> None:
    title = PIPELINE_TITLE_START.format(version=PIPELINE_VERSION)
    engine_note = PIPELINE_ENGINE_NOTE.format(version=PIPELINE_VERSION)
    log_banner(f"{title}\n\n{engine_note}", color=FG.CYAN, line_color=FG.BLUE, )

  def _prepare_infrastructure(self, steps: StepLogger) -> None:
    steps.step(PIPELINE_STEP_ENSURE_DIRS)
    ensure_directories()

  def _load_data(self, steps: StepLogger, options: PipelineOptions) -> QuestionData:
    steps.step(PIPELINE_STEP_LOADING_DATA.format(path=options.data_file))
    return self.data_loader.load_csv_data(options.data_file)

  def _compute_summary(self, steps: StepLogger, question_data: QuestionData) -> DatasetSummary:
    steps.step(PIPELINE_STEP_COMPUTE_STATS)
    return compute_statistics(question_data.df)

  # [수정 5] ChartExporter 사용 및 export 메서드 호출
  def _generate_charts(self, steps: StepLogger, summary: DatasetSummary, options: PipelineOptions) -> None:
    if not options.charts_dir:
      self.logger.warning("차트 생성이 활성화되었으나 저장 경로(charts_dir)가 설정되지 않았습니다.")
      return

    steps.step(PIPELINE_STEP_GENERATE_CHARTS)
    self.chart_exporter.export(summary, output_dir=options.charts_dir)

  # [수정 6] Json/Excel Exporter 사용 및 options 경로 활용
  def _write_artifacts(self, steps: StepLogger, summary: DatasetSummary, options: PipelineOptions) -> str:
    steps.step(PIPELINE_STEP_SAVE_ARTIFACTS)

    # 1. JSON 저장
    if options.json_dir:
      steps.step(PIPELINE_STEP_WRITE_JSON.format(target=options.json_dir.name))
      self.json_exporter.export(summary, target_path=options.json_dir)

      # (옵션) 만약 summaries_dir(공유용)가 별도로 설정되어 있다면 추가 저장
      if options.summaries_dir:
        self.json_exporter.export(summary, target_path=options.summaries_dir)

    # 2. Excel 저장
    excel_result = "Skipped"
    if options.generate_excel and options.xlsx_dir:
      def excel_progress_callback(current, total, message):
        steps.progress(current, total, message, channel="Excel")

      # 저장할 전체 파일 경로 생성
      filename = "analysis_report.xlsx"
      filepath = options.xlsx_dir / filename

      result_path = self.excel_exporter.export(
        summary,
        filepath=filepath,
        progress_callback=excel_progress_callback
      )

      if result_path:
        excel_result = str(result_path)

    return excel_result

  def _log_completion(self, excel_path: str, options: PipelineOptions) -> None:
    log_banner(
      PIPELINE_TITLE_COMPLETE,
      color=FG.GREEN,
      line_color=FG.GREEN,
    )

    if options.json_dir:
      self.logger.info(PIPELINE_LOG_SAVED.format(label="JSON", path=options.json_dir))

    if options.charts_dir and options.generate_charts:
      self.logger.info(PIPELINE_LOG_SAVED.format(label="Charts", path=options.charts_dir))

    if excel_path != "Skipped":
      self.logger.info(PIPELINE_LOG_SAVED.format(label="Excel Report", path=excel_path))

    log_banner(PIPELINE_TITLE_FINISHED, color=FG.YELLOW, line_color=FG.YELLOW)
