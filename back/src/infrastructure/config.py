import os
from pathlib import Path
from typing import Final, List

# 프로젝트 루트
ROOT_DIR: Final[Path] = Path(__file__).parent.parent.parent.resolve()

# 기본 설정
ENCODING: Final[str] = "utf-8"

# CSV 로딩 시 날짜로 파싱할 컬럼(Data Loader에서 필요)
DATE_COLUMNS: Final[List[str]] = ["created_at", "updated_at", "CreatedAt"]

# 데이터 입력
DATA_DIR: Final[Path] = ROOT_DIR / "data"
CODING_DATA_DIR: Final[Path] = DATA_DIR / "coding-questions-dataset"
DATA_FILE: Final[Path] = CODING_DATA_DIR / "questions_dataset.csv"

# 산출물 저장
ARTIFACTS_DIR: Final[Path] = ROOT_DIR / "artifacts"
SUMMARIES_DIR: Final[Path] = ARTIFACTS_DIR / "summaries"
CHARTS_DIR: Final[Path] = ARTIFACTS_DIR / "charts"
OUTPUT_BACK_DIR: Final[Path] = SUMMARIES_DIR / "summary.json"

# 프론트 경로에 산출물 저장
FRONTEND_DIR: Final[Path] = ROOT_DIR.parent / "front"
FRONTEND_PUBLIC_DIR: Final[Path] = FRONTEND_DIR / "public"
FRONTEND_SHARED_DIR: Final[Path] = FRONTEND_DIR / "src" / "shared" / "data"
FRONTEND_SUMMARY_FILE: Final[Path] = FRONTEND_DIR / "summary.json"


# artifacts 디렉토리를 자동으로 생성하는 유틸
def ensure_directories() -> None:
  ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
  SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
  CHARTS_DIR.mkdir(parents=True, exist_ok=True)

