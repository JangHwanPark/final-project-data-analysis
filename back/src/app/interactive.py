from __future__ import annotations

from pathlib import Path
import questionary

# MAC 설정 (윈도우 모듈)
try:
  # 윈도우 콘솔에서 버퍼가 없는 환경일 때 발생하는 예외
  from prompt_toolkit.output.win32 import NoConsoleScreenBufferError
except (ImportError, AssertionError):
  # 맥/리눅스 등 win32 모듈이 없을 때를 위한 더미 예외 클래스
  class NoConsoleScreenBufferError(Exception):
    """윈도우 콘솔 버퍼 관련 예외 더미 클래스 (비윈도우 환경용)."""
    pass

from typing import Any, Dict, Set, List, Tuple, Optional
from constants.path import DataPaths
from infrastructure.logging import get_logger

from constants.path import (
  ArtifactsPaths,
  FrontendPaths,
)

from app_types.pipelien import AnalysisScope, OutputTarget
from app.pipeline_options import (
  PipelineOptions,
  FrontendJsonTarget,
  default_frontend_targets
)

from constants.interactive import (
  OUTPUT_TARGET_CHOICES,
  OUTPUT_TARGET_MAP,
  ANALYSIS_SCOPE_CHOICES,
  ANALYSIS_SCOPE_DEFAULT,
  ANALYSIS_SCOPE_MAP,
  ENGINE_CHOICES,
  ENGINE_DEFAULT,
  ENGINE_MAP
)

logger = get_logger("interactive-fallback")


# ====================================================
# Questionary 기반 입력 함수들
# ====================================================
def ask_engine() -> str:
  # 데이터 로딩 엔진을 선택하는 인터랙티브 질문 함수.
  # choices 내 데이터를 중 하나를 고르게 하고
  # 선택한 값?중 하나의 짧은 문자열로 정제해서 반환한다.
  engine_choice = questionary.select(
    "데이터 로딩 엔진을 선택하세요.",
    choices=ENGINE_CHOICES,
    default=ENGINE_DEFAULT,
  ).ask()

  # 선택된 문자열을 기반으로 실제 엔진 키워드로 매핑
  return ENGINE_MAP[engine_choice]


# ====================================================
# CSV 데이터 파일 경로를 선택하는 인터랙티브 질문 함수.
# 기본 CSV(DATA_FILE)를 쓸지 묻고
# 아니오를 선택하면 경로를 직접 입력/선택하게 한다.
# ====================================================
def ask_data_file(engine: str) -> Path:
  if engine == "csv":
    file_type_label = "CSV"
  elif engine == "json":
    file_type_label = "JSON"
  else:
    file_type_label = "데이터"

  use_default = questionary.confirm(
    f"기본 {file_type_label} 파일을 사용할까요?\n  -> {DataPaths.QUESTIONS_FILE}",
    default=True,
  ).ask()

  if use_default:
    return DataPaths.QUESTIONS_FILE

  path_str = questionary.path(
    f"분석할 {file_type_label} 파일 경로를 입력하거나 선택하세요.",
    default=str(DataPaths.QUESTIONS_FILE),
  ).ask()

  # 사용자가 취소(Ctrl+C 등)하거나 None/빈 문자열을 입력한 경우
  if not path_str:
    questionary.print(
      f"입력이 없어서 기본 {file_type_label} 파일을 사용합니다.",
      style="italic",
    )
    return DataPaths.QUESTIONS_FILE

  return Path(path_str)


# ====================================================
# [분석 범위 선택]UI 선택값(영문 라벨)을 ANALYSIS_SCOPE_MAP을 통해
# 'full' | 'basic' | 'custom' 중 하나(AnalysisScope)로 정규화하여 반환
# ====================================================
def ask_analysis_scope() -> AnalysisScope:
  scope = questionary.select(
    "Select analysis scope.",
    choices=ANALYSIS_SCOPE_CHOICES,
    default=ANALYSIS_SCOPE_DEFAULT,
  ).ask()

  return ANALYSIS_SCOPE_MAP[scope]


# ====================================================
# 어떤 형식으로 결과를 저장할지 선택 (복수 선택 가능)
# return - {"json", "excel"} / {"json", "charts"} ...
# ====================================================
def ask_output_targets() -> Set[OutputTarget]:
  selected = questionary.checkbox(
    "Select output targets.",
    choices=OUTPUT_TARGET_CHOICES,
  ).ask()

  # 사용자가 전부 해제하는 경우 안전 장치
  if not selected:
    questionary.print("선택이 없어 기본값(JSON + Excel)을 사용합니다.", style="italic")
    selected = ["JSON", "Excel"]

  return {OUTPUT_TARGET_MAP[label] for label in selected}


# ====================================================
# output_targets에 기반해 차트 생성 여부를 결정하는 헬퍼.
# (필요하다면 나중에 별도 옵션으로 분리 가능)
# ====================================================
def ask_generate_charts_from_targets(output_targets: set[str]) -> bool:
  return "charts" in output_targets


# ====================================================
# output_targets에 기반해 Excel 생성 여부를 결정하는 헬퍼.
# ====================================================
def ask_generate_excel_from_targets(output_targets: set[str]) -> bool:
  return "excel" in output_targets


# ====================================================
# 차트 이미지 생성 여부를 묻는 함수. (기본값은 True)
# ====================================================
def ask_generate_charts() -> bool:
  return questionary.confirm(
    "차트 이미지를 생성할까요?", default=True
  ).ask()


# ====================================================
# Excel 리포트 생성 여부를 묻는 함수. (기본값은 True)
# ====================================================
def ask_generate_excel() -> bool:
  return questionary.confirm(
    "Excel 리포트를 생성할까요?", default=True
  ).ask()


# ====================================================
# 저장 경로 설정 함수
# 기본 구조(artifacts/...)를 쓸지 커스텀 경로를 쓸지 묻는다.
# 저장 경로를 결정하여 PipelineOptions에 들어갈 인자 딕셔너리를 반환
# ====================================================
def ask_artifact_paths(output_targets: Set[OutputTarget], generate_charts: bool, generate_excel: bool) -> Dict[str, Any]:
  # 기본 구조 사용 여부 질문
  use_default = questionary.confirm(
    "결과물을 기본 'artifacts/' 폴더 구조(charts, json, xlsx)에 저장할까요?",
    default=True
  ).ask()

  paths: Dict[str, Optional[Path]] = {
    "json_dir": None,
    "charts_dir": None,
    "xlsx_dir": None,
    "summaries_dir": None
  }

  # ---------------------------------------------------------
  # 기본 경로를 쓴다고 하면, 여기서 구체적인 경로를 지정하지 않고 None으로 둠
  # 그러면 pipeline.py 내부에서 get_target_directories()를 호출하여
  # 환경(Dev/Exe)에 맞는 다중 경로를 자동으로 가져옴
  # ---------------------------------------------------------
  if use_default:
    pass
  # ---------------------------------------------------------
  # 사용자 지정 경로 입력 (단일 폴더 지정)
  # 사용자가 직접 입력한 경우에는 그 폴더 하나에만 저장됩니다.
  # ---------------------------------------------------------
  else:
    if "json" in output_targets:
      j_path = questionary.path("JSON 저장 루트 폴더:", default=str(ArtifactsPaths.JSON)).ask()
      paths["json_dir"] = Path(j_path)
      paths["summaries_dir"] = Path(j_path)

    if generate_charts:
      c_path = questionary.path("차트 저장 폴더:", default=str(ArtifactsPaths.CHARTS)).ask()
      paths["charts_dir"] = Path(c_path)

    if generate_excel:
      x_path = questionary.path("Excel 저장 폴더:", default=str(ArtifactsPaths.XLSX)).ask()
      paths["xlsx_dir"] = Path(x_path)

  return paths


# ====================================================
# 사용자가 선택한 옵션을 요약해서 출력
# ====================================================
def print_summary(
        data_file: Path,
        engine: str,
        analysis_scope: str,
        output_targets: set[str],
        json_dir: Path,
        charts_dir: Path,
        xlsx_dir: Path,
        frontend_json_targets: List[FrontendJsonTarget],
) -> None:
  questionary.print(
    "\n[선택한 옵션 요약]",
    style="bold",
  )
  questionary.print(f" - data_file: {data_file}")
  questionary.print(f" - engine: {engine}")
  questionary.print(f" - analysis_scope: {analysis_scope}")
  questionary.print(f" - output_targets: {sorted(output_targets)}\n")
  questionary.print(f" - json_dir: {json_dir}")
  questionary.print(f" - charts_dir: {charts_dir}")
  questionary.print(f" - xlsx_dir: {xlsx_dir}")
  questionary.print(f" - frontend_json_targets (Total: {len(frontend_json_targets)}):")
  for target in frontend_json_targets:
    # 경로와 파일명 같이 표시
    questionary.print(f"   -> [{target.scope.value}] {target.target_dir} / {target.filename}")
  questionary.print("")


# ====================================================
# 선택한 옵션으로 실제 파이프라인을 실행할지 최종 확인하는 함수.
# 사용자가 아니오를 선택하면 SystemExit로 종료한다.
# ====================================================
def confirm_run() -> None:
  ok = questionary.confirm(
    "이 설정으로 파이프라인을 실행할까요?",
    default=True,
  ).ask()

  if not ok:
    raise SystemExit("사용자가 파이프라인 실행을 취소했습니다.")


# ====================================================
# questionary를 사용하여 인터랙티브하게 PipelineOptions를 구성하는 상위 함수.
# 개별 질문 함수들을 호출해서 옵션들을 모두 모은 뒤 PipelineOptions를 반환.
#
# 전체 플로우
# 1. 엔진 선택 (csv/json/db)
# 2. 엔진 타입에 맞는 데이터 파일/소스 경로 선택
# 3. 분석 범위 선택 (full/basic/custom)
# 4. 출력 타깃 선택 (json/excel/charts)
# 5. output_targets를 기반으로 generate_charts / generate_excel 계산
# 6. 요약 출력 및 실행 여부 최종 확인
# 7. PipelineOptions 생성 후 반환
# ====================================================
def ask_user_with_questionary() -> PipelineOptions:
  engine = ask_engine()
  data_file = ask_data_file(engine)
  analysis_scope = ask_analysis_scope()
  output_targets = ask_output_targets()
  # ---------------------------------------------------------
  # [중복 질문] 차트/엑셀 생성 여부 판단
  # (output_targets에 포함되어 있고 + 사용자에게 추가 질문)
  # ---------------------------------------------------------
  # gen_charts = False
  # if ask_generate_charts_from_targets(output_targets):
  #   gen_charts = ask_generate_charts()
  #
  # gen_excel = False
  # if ask_generate_excel_from_targets(output_targets):
  #   gen_excel = ask_generate_excel()
  # ---------------------------------------------------------
  # 경로 질문 함수 호출!
  # 사용자가 이미 위에서 체크박스로 선택했으니, 포함 여부만 확인
  # ---------------------------------------------------------
  gen_charts = "charts" in output_targets
  gen_excel = "excel" in output_targets
  paths = ask_artifact_paths(output_targets, gen_charts, gen_excel)
  # ---------------------------------------------------------
  # 결과 변수 할당 (None이 들어올 수 있음)
  # ---------------------------------------------------------
  json_dir = paths["json_dir"]
  charts_dir = paths["charts_dir"]
  xlsx_dir = paths["xlsx_dir"]
  frontend_targets = default_frontend_targets(analysis_scope=analysis_scope)
  # ---------------------------------------------------------
  # 최종 요약 출력
  # ---------------------------------------------------------
  print_summary(
    data_file=data_file,
    engine=engine,
    analysis_scope=analysis_scope,
    output_targets=output_targets,
    json_dir=json_dir,
    charts_dir=charts_dir,
    xlsx_dir=xlsx_dir,
    frontend_json_targets=frontend_targets,
  )
  # ---------------------------------------------------------
  # 실행 여부 최종 확인
  # ---------------------------------------------------------
  confirm_run()
  # ---------------------------------------------------------
  # PipelineOptions 인스턴스 생성 후 반환
  # ---------------------------------------------------------
  return PipelineOptions(
    data_file=data_file,
    engine=engine,
    analysis_scope=analysis_scope,
    output_targets=output_targets,
    json_dir=json_dir,
    charts_dir=charts_dir,
    xlsx_dir=xlsx_dir,
    frontend_json_targets=frontend_targets,
  )


# ====================================================
# fallback (questionary 불가 시)
# questionary를 사용할 수 없는 환경(예: 일부 윈도우 콘솔)에서
# input() 기반으로 최소한의 옵션만 받아서 PipelineOptions를 구성하는 함수.
# ====================================================
def ask_user_with_fallback() -> PipelineOptions:
  logger.warning("questionary를 사용할 수 없는 환경입니다. 텍스트 모드로 진행합니다.\n")

  # CSV 경로 입력
  path_input = input(f"분석할 CSV 경로 (기본: {DataPaths.QUESTIONS_FILE}): ")
  data_file = Path(path_input) if path_input else DataPaths.QUESTIONS_FILE
  logger.info(f"데이터 파일 설정됨: {data_file}")

  # 현재는 csv만 지원 (엔진 선택은 생략)
  logger.info("데이터 로딩 엔진: csv(default)")
  engine = "csv"
  analysis_scope = ask_analysis_scope()
  output_targets = ask_output_targets()

  return PipelineOptions(
    data_file=data_file,
    engine=engine,
    analysis_scope=analysis_scope,
    output_targets=output_targets,
  )


# ====================================================
# 외부에서 호출하는 진입점 함수.
# questionary 기반 인터랙티브 UI를 시도하고
# NoConsoleScreenBufferError 발생 시 input() 기반 fallback으로 전환
# 윈도우 특정 환경 등에서 questionary가 동작하지 않을 때만 fallback 사용
# ====================================================
def ask_user_for_options() -> PipelineOptions:
  try:
    return ask_user_with_questionary()
  except NoConsoleScreenBufferError:
    return ask_user_with_fallback()
