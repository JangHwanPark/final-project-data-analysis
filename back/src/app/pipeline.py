from app_types.pipelien import AnalysisScope
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
  PIPELINE_LOG_SAVED,
  PIPELINE_ENGINE_NOTE,
)
from constants.path import (
  ensure_directories,
)
from domain.entities.data_model import QuestionData, DatasetSummary
from domain.service.metrics import compute_statistics
from infrastructure.data_loader import DataLoader
from infrastructure.logging import StepLogger, log_banner
from infrastructure.logging.style import FG
from presentation.exporters import JsonExporter, ExcelExporter, ChartExporter
from .pipeline_options import PipelineOptions, default_frontend_targets
from dataclasses import replace

# ====================================================
# 애플리케이션 계층의 데이터 분석 파이프라인 유즈케이스.
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

  # ====================================================
  # 실행함수
  # ====================================================
  def run(self, options: PipelineOptions) -> None:
    steps = StepLogger(logger_name=self.logger.name)
    self._log_start_banner()
    self._prepare_infrastructure(steps)
    question_data = self._load_data(steps, options)

    if question_data is None or question_data.df.empty:
      self.logger.error(PIPELINE_MESSAGE_FATAL_EMPTY_DATA)
      return

    summary = self._compute_summary(steps, question_data)

    # options 객체를 helper 메서드에 전달 (경로 정보가 options에 있음)
    if options.charts_dir:
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

  # ==============================================================
  # [private helper methods] ChartExporter 사용 및 export 메서드 호출
  # ==============================================================
  def _generate_charts(self, steps: StepLogger, summary: DatasetSummary, options: PipelineOptions) -> None:
    if not options.charts_dir:
      self.logger.warning("차트 생성이 활성화되었으나 저장 경로(charts_dir)가 설정되지 않았습니다.")
      return

    steps.step(PIPELINE_STEP_GENERATE_CHARTS)
    self.chart_exporter.export(summary, output_dir=options.charts_dir)

  # ==============================================================
  # [private helper methods] Json/Excel Exporter 사용 및 options 경로 활용
  # ==============================================================
  def _write_artifacts(
          self,
          steps: StepLogger,
          summary: DatasetSummary,
          options: PipelineOptions
  ) -> str:
    steps.step(PIPELINE_STEP_SAVE_ARTIFACTS)
    # ArtifactsPaths.JSON에 저장할 타겟 리스트를 생성(백업용)
    artifacts_json_targets = []

    if options.json_dir:
      # Frontend Targets 리스트를 가져와서 경로만 options.json_dir로 변경하여 복제
      for target in options.frontend_json_targets:
        artifacts_json_targets.append(replace(target, target_dir=options.json_dir))

    # JSON 저장 루프 통합 (백엔드 아티팩트 + 프론트엔드)
    all_json_targets = artifacts_json_targets + options.frontend_json_targets
    if all_json_targets:
      for target in all_json_targets:
        # 타겟 경로가 백엔드 아티팩트인지, 프론트엔드인지 구분하여 로그 출력
        location = "Artifacts" if target.target_dir == options.json_dir else "Frontend"
        steps.step(f"Saving [{target.scope.value}] to {location}: {target.filename}")

        # 경로 생성 보장
        target.target_dir.mkdir(parents=True, exist_ok=True)

        if target.keys:
          # Keys가 있으면: 탭별 데이터 분할 저장 (subset)
          self.json_exporter.export_subset(
            summary,
            target_dir=target.target_dir,
            filename=target.filename,
            keys=target.keys,
          )
        else:
          # Keys가 없으면: 전체 데이터 저장 (FULL/RAW Data)
          self.json_exporter.export(
            summary,
            target_path=target.target_dir,
            filename=target.filename,
            scope=target.scope,
          )

    # Excel 저장 분리 (탭별 파일 생성)
    excel_result = "Skipped"
    if options.xlsx_dir:
      # Excel 파일 분리 저장: overview, difficulty, tags, structure 4개의 엑셀 파일 생성
      excel_targets = default_frontend_targets(AnalysisScope.FULL)

      def excel_progress_callback(current, total, message):
        steps.progress(current, total, message, channel="Excel")

      for idx, target in enumerate(excel_targets):
        # 엑셀 파일명은 JSON 파일명과 동일하게 사용(예: overview.xlsx)
        filename = f"{target.filename}.xlsx"
        filepath = options.xlsx_dir / filename
        steps.progress(idx + 1, len(excel_targets), f"Writing {filename}")
        # TODO
        # ExcelExporter는 JSON처럼 subset 추출 로직이 없으므로,
        # 현재는 모든 엑셀 파일에 전체 Summary를 저장하는 방식으로 구현합니다.
        # (나중에 ExcelExporter에 subset 추출 로직을 추가해야 함)
        # 콜백은 ExcelExporter 내부에서 관리 필요
        self.excel_exporter.export(summary, filepath=filepath, progress_callback=excel_progress_callback)
        # 마지막 경로만 저장
        excel_result = str(options.xlsx_dir)

    return excel_result

  def _log_completion(self, excel_path: str, options: PipelineOptions) -> None:
    log_banner(
      PIPELINE_TITLE_COMPLETE,
      color=FG.GREEN,
      line_color=FG.GREEN,
    )

    if options.json_dir:
      # JSON 디렉토리에는 5개의 파일이 저장됨을 로깅
      self.logger.info(PIPELINE_LOG_SAVED.format(label="JSON", path=options.json_dir))

    if options.charts_dir and options.charts_dir:
      self.logger.info(PIPELINE_LOG_SAVED.format(label="Charts", path=options.charts_dir))

    if excel_path != "Skipped":
      # 엑셀도 분할되어 저장되었음을 로깅
      self.logger.info(PIPELINE_LOG_SAVED.format(label="Excel Report", path=excel_path))

    log_banner(PIPELINE_TITLE_FINISHED, color=FG.YELLOW, line_color=FG.YELLOW)
