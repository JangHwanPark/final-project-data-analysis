from __future__ import annotations

from pathlib import Path
import os
import sys


def ensure_venv(
        project_root: Path | None = None,
        module_to_run: str | None = None,
) -> None:
  """
  - 현재 프로세스가 가상환경(.venv) 안에서 실행 중인지 확인하고
  - 아니라면 .venv의 python으로 현재 스크립트를 다시 실행한 뒤 종료.

  :param project_root: 프로젝트 루트(여기에 .venv가 있다고 가정). None이면 이 파일 기준으로 계산.
  :param module_to_run: `python -m 모듈` 형태로 다시 실행하고 싶을 때 사용.
  """
  # 이미 가상환경이면 그대로 진행
  if sys.prefix != getattr(sys, "base_prefix", sys.prefix):
    return

  # 프로젝트 루트 추론 (현재 파일: back/src/infrastructure/runtime/venv.py 라고 가정)
  if project_root is None:
    # .../back/src/infrastructure/runtime/venv.py
    # parents[0] = runtime
    # parents[1] = infrastructure
    # parents[2] = src
    # parents[3] = back  <-- 여기를 프로젝트 루트로 가정
    project_root = Path(__file__).resolve().parents[2]

  venv_dir = project_root / ".venv"

  if os.name == "nt":
    python_bin = venv_dir / "Scripts" / "python.exe"
  else:
    python_bin = venv_dir / "bin" / "python"

  if not python_bin.exists():
    print(
      f"[ensure_venv] .venv 환경을 찾을 수 없습니다.\n"
      f"  예상 경로: {python_bin}\n"
      f"먼저 아래 명령으로 가상환경을 생성 후 패키지를 설치하세요:\n"
      f"  python -m venv .venv\n"
      f"  .venv\\Scripts\\pip install -r requirements.txt\n"
    )
    sys.exit(1)

  # 여기까지 왔으면: venv는 있는데 현재는 시스템 파이썬에서 실행 중
  # → venv의 python으로 재실행
  if module_to_run:
    # python -m app.main_interactive 같은 형태로 재실행
    args = [str(python_bin), "-m", module_to_run, *sys.argv[1:]]
  else:
    # 현재 스크립트 경로 그대로 재실행
    args = [str(python_bin), *sys.argv]

  # 디버깅용으로 찍어보고 싶으면 아래 주석 해제
  print(f"[ensure_venv] Re-exec: {' '.join(args)}")

  # 현재 프로세스를 이 프로세스로 교체
  os.execv(args[0], args)
