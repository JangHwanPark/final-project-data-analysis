from __future__ import annotations

from pathlib import Path
import questionary

# MAC 설정 (윈도우 모듈)
try:
  from prompt_toolkit.output.win32 import NoConsoleScreenBufferError
except (ImportError, AssertionError):
  class NoConsoleScreenBufferError(Exception):
    pass

from app.options import PipelineOptions
from infrastructure.config import DATA_FILE
from infrastructure.logging import get_logger

logger = get_logger("interactive-fallback")

def ask_user_for_options() -> PipelineOptions:
  try:
    # 데이터 파일 선택 (기본 CSV 그대로 쓸지, 다른 경로 쓸지)
    use_default = questionary.confirm(
      f"기본 CSV 파일을 사용할까요?\n  -> {DATA_FILE}",
      default=True,
    ).ask()

    if use_default:
      data_file = DATA_FILE
    else:
      path_str = questionary.path(
        "분석할 CSV 파일 경로를 입력하거나 선택하세요:",
        default=str(DATA_FILE),
      ).ask()
      data_file = Path(path_str)

    # 엔진 선택 (지금은 CSV만 의미 있음, 구조만 잡아두기)
    engine = questionary.select(
      "데이터 로딩 엔진을 선택하세요:",
      choices=[
        "csv (기본)",
        "json (미구현)",
        "db (미구현)",
      ],
      default="csv (기본)",
    ).ask()

    # 문자열 정리
    if engine.startswith("csv"):
      engine = "csv"
    elif engine.startswith("json"):
      engine = "json"
    else:
      engine = "db"

    # 차트 생성 여부
    generate_charts = questionary.confirm(
      "차트 이미지를 생성할까요?", default=True
    ).ask()

    # 엑셀 리포트 생성 여부
    generate_excel = questionary.confirm(
      "Excel 리포트를 생성할까요?", default=True
    ).ask()

    # 요약 한번 보여주기
    questionary.print(
      "\n[선택한 옵션 요약]",
      style="bold",
    )
    questionary.print(f" - data_file: {data_file}")
    questionary.print(f" - engine: {engine}")
    questionary.print(f" - charts: {generate_charts}")
    questionary.print(f" - excel: {generate_excel}\n")

    ok = questionary.confirm("이 설정으로 파이프라인을 실행할까요?", default=True).ask()
    if not ok:
      raise SystemExit("사용자가 파이프라인 실행을 취소했습니다.")

    return PipelineOptions(
      data_file=data_file,
      generate_charts=generate_charts,
      generate_excel=generate_excel,
      engine=engine,
    )
  except NoConsoleScreenBufferError:
    # fallback: 그냥 input()으로 물어보기
    logger.warning("questionary를 사용할 수 없는 환경입니다. 텍스트 모드로 진행합니다.\n")

    # CSV 경로 입력
    path_input = input(f"분석할 CSV 경로 (기본: {DATA_FILE}): ")
    data_file = Path(path_input) if path_input else DATA_FILE
    logger.info(f"데이터 파일 설정됨: {data_file}")

    # 지원하는 엔진 안내(현재 csv만 가능)
    logger.info("데이터 로딩 엔진: csv(default)")
    engine = "csv"

    # 차트/엑셀은 기본 True
    logger.info("차트 생성: True")
    logger.info("Excel 생성: True")
    generate_charts = True
    generate_excel = True

    return PipelineOptions(
      data_file=data_file,
      generate_charts=generate_charts,
      generate_excel=generate_excel,
      engine=engine,
    )
