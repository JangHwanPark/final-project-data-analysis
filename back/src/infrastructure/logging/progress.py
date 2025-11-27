import sys
import time


def draw_progress_bar(current: int, total: int, prefix: str = "", bar_length: int = 40):
  # 실시간 갱신되는 콘솔 프로그래스바 출력 (로그파일에는 남기지 않음)
  # ex. [#####-----] 40%

  percent = current / total
  filled = int(bar_length * percent)
  bar = "#" * filled + "-" * (bar_length - filled)
  progress = f"{prefix} [{bar}] {percent * 100:5.1f}%"

  sys.stdout.write("\r" + progress)
  sys.stdout.flush()

  if current >= total:
    sys.stdout.write("\n")
