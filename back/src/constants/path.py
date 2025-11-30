from pathlib import Path
from typing import Final

# =================================================================
# 프로젝트 ROOT 폴더
# 주의: 이 파일의 위치에 따라 .parent 개수가 달라집니다.
# 예: src/constants/paths.py 라면 루트는 2단계 상위
# =================================================================
ROOT_DIR: Final[Path] = Path(__file__).parents[2].resolve()


# =================================================================
# [폴더 구조 정의] 원본 데이터 (Data) 경로
# =================================================================
class DataPaths:
  ROOT: Final[Path] = ROOT_DIR / "data"
  QUESTIONS_DIR: Final[Path] = ROOT / "coding-questions-dataset"
  QUESTIONS_FILE: Final[Path] = QUESTIONS_DIR / "questions_dataset.csv"


# =================================================================
# [폴더 구조 정의] 백엔드 산출물 (Artifacts) 경로
# =================================================================
class ArtifactsPaths:
  ROOT = ROOT_DIR / "artifacts"
  CHARTS = ROOT / "charts"
  JSON = ROOT / "json"
  SUMMARIES = ROOT / "summaries"
  XLSX = ROOT / "xlsx"


# =================================================================
# [폴더 구조 정의] 프론트엔드 연동 (Frontend) 경로
# =================================================================
class FrontendPaths:
  # backend 루트의 상위(모노레포 루트)로 가서 front로 진입
  ROOT: Final[Path] = ROOT_DIR.parent / "front"

  # 데이터 디렉토리
  PUBLIC_DATA_DIR: Final[Path] = ROOT / "public" / "data"
  SHARED_DATA_DIR: Final[Path] = ROOT / "src" / "shared" / "data"

  # 실제 저장될 파일 경로 (DIR -> FILE로 명칭 변경 추천)
  PUBLIC_SUMMARY_FILE: Final[Path] = PUBLIC_DATA_DIR / "summary.json"
  SHARED_SUMMARY_FILE: Final[Path] = SHARED_DATA_DIR / "summary.json"


# =================================================================
# artifacts 디렉토리를 자동으로 생성하는 유틸
# =================================================================
def ensure_directories() -> None:
  # 파이프라인을 실행하기 전에 모든 출력 디렉토리가 있는지 확인
  dirs_to_ensure = [
    ArtifactsPaths.ROOT,
    ArtifactsPaths.JSON,
    ArtifactsPaths.CHARTS,
    ArtifactsPaths.XLSX,
    FrontendPaths.SHARED_DATA_DIR,
  ]
  for d in dirs_to_ensure:
    d.mkdir(parents=True, exist_ok=True)
