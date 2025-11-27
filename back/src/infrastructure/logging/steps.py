from infrastructure.logging import get_logger
import time

class StepLogger:
  # 파이프라인 단계별 진행 상황을 [현재/전체] 형식으로 로깅
  def __init__(self, total_steps: int, logger_name: str = "pipeline"):
    self.total = total_steps
    self.current = 0
    self.logger = get_logger(logger_name)

  def step(self, message: str):
    # 자동으로 [x/total] prefix를 붙여서 로그를 출력
    self.current += 1
    prefix = f"[{self.current}/{self.total}]"
    self.logger.info(f"{prefix} {message}")
    time.sleep(0.1)
