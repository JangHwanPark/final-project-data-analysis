import sys
from pathlib import Path
from typing import List


# 오타 방지를 위한 상수 정의
class ArtifactType:
  JSON = "json"
  EXCEL = "excel"
  CHART = "chart"


# ====================================================
# 실행 환경(Frozen/Dev)과 아티팩트 타입에 따라 저장할 경로 리스트를 반환
# EXE 실행 시: 사용자 바탕화면/{dir_name}
# 개발 실행 시: 프로젝트 루트/output/{dir_name}
# ====================================================
# Args
# - artifact_type: 저장할 파일 타입 (json, excel, chart)
# - custom_root: 사용자가 직접 지정한 루트 경로 (없으면 기본 로직 따름)
# - dir_name: 배포 환경에서 생성할 최상위 폴더명
# ====================================================
def get_target_directories(
        artifact_type: str,
        custom_root: Path = None,
        dir_name: str = "분석결과_Output"
) -> List[Path]:
  # EXE로 패키징된 상태인지 확인 (Frozen 상태)
  is_frozen = getattr(sys, 'frozen', False)
  targets = []

  # ====================================================
  # 사용자가 커스텀 경로를 지정했을 경우 (우선순위 높음, 단일 경로)
  # 커스텀경로/json, 커스텀경로/excel 등으로 하위 폴더 자동 구분
  # ====================================================
  if custom_root:
    targets.append(custom_root)
  # ====================================================
  # 배포 환경 (Frozen: EXE 실행) - 바탕화면 저장
  # ====================================================
  elif is_frozen:
    # 배포 환경: 사용자 바탕화면 경로 찾기
    # Path.home()은 'C:/Users/사용자명'을 반환합니다.
    desktop = Path.home() / "Desktop"
    base_output = desktop / dir_name
    targets.append(base_output / artifact_type)
  # ====================================================
  # 개발 환경 (Source 실행) - 프로젝트 구조에 맞춰 분산 저장
  # current_path: 실행 위치(cwd)를 프로젝트 루트로 가정
  # ====================================================
  else:
    current_file = Path(__file__).resolve()
    # ---------------------------------------------------------
    # 부모를 4번 타고 올라가야 root가 나옴
    # 1. infrastructure -> 2. src -> 3. back -> 4. root
    # ---------------------------------------------------------
    project_root = current_file.parent.parent.parent.parent
    # [디버깅용] 경로가 제대로 잡혔는지 콘솔에서 확인
    # print(f"DEBUG: Project Root is -> {project_root}")
    if artifact_type == ArtifactType.JSON:
      targets = [
        project_root / "front/public/data",  # 프론트 public
        project_root / "front/src/shared/data",  # 프론트 shared (src가 빠졌었음 확인 필요!)
        project_root / "back/artifacts/json"  # 백엔드
      ]
    elif artifact_type == ArtifactType.EXCEL:
      targets = [project_root / "back/artifacts/xlsx"]
    elif artifact_type == ArtifactType.CHART:
      targets = [project_root / "back/artifacts/charts"]
    # ---------------------------------------------------------
    # 폴더 생성 보장 (없으면 생성)
    # ---------------------------------------------------------
    for path in targets:
      try:
        path.mkdir(parents=True, exist_ok=True)
      except Exception as e:
        print(f"[Warning] 경로 생성 실패: {path} - {e}")

  return targets
