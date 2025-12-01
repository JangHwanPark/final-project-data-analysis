from __future__ import annotations
from pathlib import Path
import sys


# ====================================================
# PyInstaller 등으로 빌드된 exe인지 여부.
# ====================================================
def is_frozen_exe() -> bool:
  """PyInstaller 등으로 빌드된 exe인지 여부."""
  return getattr(sys, "frozen", False)


# ====================================================
# 실행 기준 디렉터리
# exe: pipeline.exe가 있는 폴더
# dev: back/src 기준으로 프로젝트 루트
# ====================================================
def get_base_dir() -> Path:
  if is_frozen_exe():
    return Path(sys.executable).parent  # pipeline.exe 위치
  else:
    # 이 파일이 infrastructure/runtime/env.py 라고 가정하면
    return Path(__file__).resolve().parents[2]  # back/src/ 까지 올라감
