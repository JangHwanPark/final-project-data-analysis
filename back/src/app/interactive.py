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

from app.options import PipelineOptions
from infrastructure.config import DATA_FILE
from infrastructure.logging import get_logger

logger = get_logger("interactive-fallback")


# ====================================================
# Questionary 기반 입력 함수들
# ====================================================
def ask_data_file() -> Path:
    # CSV 데이터 파일 경로를 선택하는 인터랙티브 질문 함수.
    # 기본 CSV(DATA_FILE)를 쓸지 묻고
    # 아니오를 선택하면 경로를 직접 입력/선택하게 한다.
    use_default = questionary.confirm(
        f"기본 CSV 파일을 사용할까요?\n  -> {DATA_FILE}",
        default=True,
    ).ask()

    if use_default:
        return DATA_FILE

    path_str = questionary.path(
        "분석할 CSV 파일 경로를 입력하거나 선택하세요:",
        default=str(DATA_FILE),
    ).ask()

    # 사용자가 취소(Ctrl+C 등)하거나 None 반환될 경우를 대비
    if not path_str:
        # 기본값으로 되돌리거나, 여기서 SystemExit를 날려도 됨
        questionary.print("입력이 없어서 기본 CSV 파일을 사용합니다.", style="italic")
        return DATA_FILE

    return Path(path_str)


def ask_engine() -> str:
    # 데이터 로딩 엔진을 선택하는 인터랙티브 질문 함수.
    # choices 내 데이터를 중 하나를 고르게 하고
    # 선택한 값?중 하나의 짧은 문자열로 정제해서 반환한다.
    engine_choice = questionary.select(
        "데이터 로딩 엔진을 선택하세요:",
        choices=[
            "csv (기본)",
            "json (미구현)",
            "db (미구현)",
        ],
        default="csv (기본)",
    ).ask()

    # 선택된 문자열을 기반으로 실제 엔진 키워드로 매핑
    if engine_choice.startswith("csv"):
        return "csv"
    elif engine_choice.startswith("json"):
        return "json"
    else:
        return "db"


def ask_generate_charts() -> bool:
    # 차트 이미지 생성 여부를 묻는 함수. (기본값은 True)
    return questionary.confirm(
        "차트 이미지를 생성할까요?", default=True
    ).ask()


def ask_generate_excel() -> bool:
    # Excel 리포트 생성 여부를 묻는 함수. (기본값은 True)
    return questionary.confirm(
        "Excel 리포트를 생성할까요?", default=True
    ).ask()


def print_summary(
    data_file: Path,
    engine: str,
    generate_charts: bool,
    generate_excel: bool,
) -> None:
    # 사용자가 선택한 옵션을 요약해서 출력해주는 함수.
    questionary.print(
        "\n[선택한 옵션 요약]",
        style="bold",
    )
    questionary.print(f" - data_file: {data_file}")
    questionary.print(f" - engine: {engine}")
    questionary.print(f" - charts: {generate_charts}")
    questionary.print(f" - excel: {generate_excel}\n")


def confirm_run() -> None:
    # 선택한 옵션으로 실제 파이프라인을 실행할지 최종 확인하는 함수.
    # 사용자가 아니오를 선택하면 SystemExit로 종료한다.
    ok = questionary.confirm(
        "이 설정으로 파이프라인을 실행할까요?",
        default=True,
    ).ask()

    if not ok:
        raise SystemExit("사용자가 파이프라인 실행을 취소했습니다.")


def ask_user_with_questionary() -> PipelineOptions:
    # questionary를 사용하여 인터랙티브하게 PipelineOptions를 구성하는 상위 함수.
    # 개별 질문 함수들을 호출해서 옵션들을 모두 모은 뒤 PipelineOptions를 반환한다.
    data_file = ask_data_file()
    engine = ask_engine()
    generate_charts = ask_generate_charts()
    generate_excel = ask_generate_excel()

    # 최종 요약 출력
    print_summary(
        data_file=data_file,
        engine=engine,
        generate_charts=generate_charts,
        generate_excel=generate_excel,
    )

    # 실행 여부 최종 확인
    confirm_run()

    return PipelineOptions(
        data_file=data_file,
        generate_charts=generate_charts,
        generate_excel=generate_excel,
        engine=engine,
    )


# ====================================================
# fallback (questionary 불가 시)
# ====================================================
def ask_user_with_fallback() -> PipelineOptions:
    # questionary를 사용할 수 없는 환경(예: 일부 윈도우 콘솔)에서
    # input() 기반으로 최소한의 옵션만 받아서 PipelineOptions를 구성하는 함수.
    logger.warning("questionary를 사용할 수 없는 환경입니다. 텍스트 모드로 진행합니다.\n")

    # CSV 경로 입력
    path_input = input(f"분석할 CSV 경로 (기본: {DATA_FILE}): ")
    data_file = Path(path_input) if path_input else DATA_FILE
    logger.info(f"데이터 파일 설정됨: {data_file}")

    # 현재는 csv만 지원 (엔진 선택은 생략)
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


# ====================================================
# public API
# ====================================================
def ask_user_for_options() -> PipelineOptions:
    # 외부에서 호출하는 진입점 함수.
    # questionary 기반 인터랙티브 UI를 시도하고
    # NoConsoleScreenBufferError 발생 시 input() 기반 fallback으로 전환
    try:
        return ask_user_with_questionary()
    except NoConsoleScreenBufferError:
        # 윈도우 특정 환경 등에서 questionary가 동작하지 않을 때만 fallback 사용
        return ask_user_with_fallback()
