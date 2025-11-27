from infrastructure.logging import get_logger
from infrastructure.logging.style import FG, STYLE, colorize
import time


class StepLogger:
  # 파이프라인 단계별 진행 상황을 [현재/전체] 형식으로 로깅
  def __init__(
          self,
          total_steps: int | None = None,
          logger_name: str = "pipeline",
          main_tag: str = "PIPELINE",
          color: str = FG.MAGENTA,
  ):
    self.total = total_steps
    self.current = 0
    self.logger = get_logger(logger_name)
    self.main_tag = main_tag if isinstance(main_tag, str) else str(main_tag)
    self.color = color

  def _main_tag_str(self) -> str:
    # [PIPELINE] 형태로 깔끔하게 만들어주는 함수
    return colorize(f"[{self.main_tag}]", STYLE.BOLD, self.color)

  def _step_prefix(self) -> str:
    # total_steps(total)가 None이면 현재까지 step count만
    if self.total is None:
      return colorize(f"[STEP {self.current}]", FG.CYAN)
    else:
      return colorize(f"[STEP {self.current}/{self.total}]", FG.CYAN)

  def step(self, message: str, emoji: str = "") -> None:
    # 자동으로 [x/total] prefix를 붙여서 로그를 출력
    self.current += 1
    prefix = f"{self._main_tag_str()} {self._step_prefix()}"

    icon = f" {emoji}" if emoji else ""
    self.logger.info(f"{prefix}{icon} {message}")
    time.sleep(0.3)

  def progress(self, current: int, total: int, message: str = "", channel: str = "Excel") -> None:
    # 세부 진행률 로그
    percentage = (current / total) * 100 if total > 0 else 0.0
    main = self._main_tag_str()
    tag = colorize(f"[{channel}]", FG.CYAN)
    self.logger.info(f"{main}{tag} {percentage:5.1f}% | {message}")
