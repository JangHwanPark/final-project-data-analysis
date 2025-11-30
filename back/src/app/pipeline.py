from pathlib import Path

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
from infrastructure.path_manager import ArtifactType
from presentation.exporters import JsonExporter, ExcelExporter, ChartExporter
from .pipeline_options import PipelineOptions, default_frontend_targets
from infrastructure.path_manager import get_target_directories, ArtifactType


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
    # ---------------------------------------------------------
    # 저장할 경로 리스트 확보
    # options.charts_dir가 있으면 custom_root로 사용, 아니면 자동 로직
    # ---------------------------------------------------------
    target_dirs = get_target_directories(
      ArtifactType.CHART,
      custom_root=options.charts_dir if options.charts_dir else None
    )

    if not target_dirs:
      return

    steps.step(PIPELINE_STEP_GENERATE_CHARTS)

    # 경로 반복 저장
    for target_path in target_dirs:
      self.logger.info(f"Generating charts to: {target_path}")
      self.chart_exporter.export(summary, output_dir=target_path)

  # ==============================================================
  # 아티팩트(JSON/Excel) 저장: 다중 경로 대응
  # ==============================================================
  def _write_artifacts(
          self,
          steps: StepLogger,
          summary: DatasetSummary,
          options: PipelineOptions
  ) -> str:
    steps.step(PIPELINE_STEP_SAVE_ARTIFACTS)
    # ---------------------------------------------------------
    # JSON 저장 (Front Public, Front Shared, Back Artifacts)
    # ---------------------------------------------------------
    # 사용자 지정 경로가 있으면 그것만, 없으면 기본 설정된 3곳 모두 가져옴
    json_destinations = get_target_directories(
      ArtifactType.JSON,
      custom_root=options.json_dir if options.json_dir else None
    )

    if json_destinations:
      for dest_path in json_destinations:
        # ---------------------------------------------------------
        # 전체 요약본(Full Summary) 저장
        # ---------------------------------------------------------
        self.json_exporter.export(
          summary,
          target_path=dest_path,
          filename="summary.json",  # 기본 파일명
          scope=AnalysisScope.FULL
        )
        # ---------------------------------------------------------
        # 프론트엔드용 분할 파일(Subsets) 저장
        # (프론트/백엔드 폴더 모두에 동일하게 저장하여 정합성 유지)
        # ---------------------------------------------------------
        for target in options.frontend_json_targets:
          # ---------------------------------------------------------
          # 키가 있으면: 부분 데이터 추출 저장 (예: overview.json)
          # ---------------------------------------------------------
          if target.keys:
            self.json_exporter.export_subset(
              summary,
              target_dir=dest_path,
              filename=target.filename,
              keys=target.keys,
            )
          # ---------------------------------------------------------
          # 키가 없으면(None): 전체 데이터 저장 (예: summary-full.json)
          # export_subset 대신 일반 export 사용
          # ---------------------------------------------------------
          else:
            self.json_exporter.export(
              summary,
              target_path=dest_path,
              filename=target.filename,
              scope=target.scope,
            )

    # ---------------------------------------------------------
    # Excel 저장: 탭별 파일 생성
    # ---------------------------------------------------------
    excel_result = "Skipped"
    # Excel 저장 경로 리스트 확보
    excel_destinations = get_target_directories(
      ArtifactType.EXCEL,
      custom_root=options.xlsx_dir if options.xlsx_dir else None
    )
    if excel_destinations:
      excel_targets = default_frontend_targets(AnalysisScope.FULL)

      def excel_progress_callback(current, total, message):
        steps.progress(current, total, message, channel="Excel")

      # 각 저장 목적지별로 반복
      for dest_path in excel_destinations:
        for idx, target in enumerate(excel_targets):
          filename = f"{target.filename}.xlsx"
          filepath = dest_path / filename

          # 로그는 한 번만 출력하거나 경로 포함해서 출력
          steps.progress(idx + 1, len(excel_targets), f"Writing {filename} to {dest_path.name}")

          self.excel_exporter.export(
            summary,
            filepath=filepath,
            progress_callback=excel_progress_callback
          )

        # 마지막 저장 경로를 결과로 반환 (로깅용)
        excel_result = str(dest_path)

    return excel_result

  # ==============================================================
  # 폴더 내부 파일 목록을 출력하는 헬퍼 메서드
  # ==============================================================
  def _print_dir_contents(self, directory: Path, label: str) -> None:
    if not directory.exists():
      return

    # 해당 폴더의 파일들만 가져오기 (폴더 제외)
    files = [f for f in directory.iterdir() if f.is_file() and not f.name.startswith('.')]

    if not files:
      return

    self.logger.info(f"📦 [{label}] Saved to: {directory}")
    for f in sorted(files):
      # 파일 크기 계산 (KB 단위)
      size_kb = f.stat().st_size / 1024
      self.logger.info(f"   └─ 📄 {f.name} ({size_kb:.1f} KB)")
    print("")  # 공백 줄 추가

  # ==============================================================
  # 완료 로그 메서드 (파일 목록 출력 기능)
  # ==============================================================
  def _log_completion(self, excel_path: str, options: PipelineOptions) -> None:
    log_banner(
      PIPELINE_TITLE_COMPLETE,
      color=FG.GREEN,
      line_color=FG.GREEN,
    )
    # ---------------------------------------------------------
    # JSON 파일 목록 출력
    # 저장된 위치들을 다시 계산해서 가져옴
    # ---------------------------------------------------------
    json_dirs = get_target_directories(
      ArtifactType.JSON,
      custom_root=options.json_dir
    )
    for path in json_dirs:
      self._print_dir_contents(path, "JSON Artifacts")
    # ---------------------------------------------------------
    # 차트 파일 목록 출력
    # ---------------------------------------------------------
    if options.charts_dir or options.frontend_json_targets:  # 차트 생성 조건
      # 차트 경로는 options에 있거나 기본 경로
      chart_dirs = get_target_directories(
        ArtifactType.CHART,
        custom_root=options.charts_dir
      )
      for path in chart_dirs:
        # 차트 폴더가 실제로 존재하고 파일이 있을 때만 출력
        self._print_dir_contents(path, "Charts")
    # ---------------------------------------------------------
    # 엑셀 파일 목록 출력
    # ---------------------------------------------------------
    excel_dirs = get_target_directories(
      ArtifactType.EXCEL,
      custom_root=options.xlsx_dir
    )
    for path in excel_dirs:
      self._print_dir_contents(path, "Excel Report")

  log_banner(PIPELINE_TITLE_FINISHED, color=FG.YELLOW, line_color=FG.YELLOW)
