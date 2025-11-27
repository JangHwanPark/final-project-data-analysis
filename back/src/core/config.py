from pathlib import Path

# 기본 설정
ENCODING = "utf-8"

# 프로젝트 루트
ROOT_DIR = Path(__file__).resolve().parents[2]

# 데이터 입력
DATA_DIR = ROOT_DIR / "data" / "coding-questions-dataset"
DATA_FILE = DATA_DIR / "questions_dataset.csv"

# 산출물 저장
ARTIFACTS_DIR = ROOT_DIR / "artifacts"
SUMMARIES_DIR = ARTIFACTS_DIR / "summaries"
CHARTS_DIR = ARTIFACTS_DIR / "charts"


# artifacts 디렉토리를 자동으로 생성하는 유틸
def ensure_directories():
  SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)
  CHARTS_DIR.mkdir(parents=True, exist_ok=True)
