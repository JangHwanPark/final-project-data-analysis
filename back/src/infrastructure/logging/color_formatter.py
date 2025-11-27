import logging
from infrastructure.logging.style import FG, STYLE, RESET


class ColorFormatter(logging.Formatter):
  # LogRecord.levelno 기반으로 메시지에 색상을 자동 적용.
  def format(self, record):
    msg = super().format(record)

    # ERROR => Red
    if record.levelno >= logging.ERROR:
      return f"{FG.RED}{STYLE.BOLD}{msg}{RESET}"

    # WARNING => Yellow
    if record.levelno == logging.WARNING:
      return f"{FG.YELLOW}{msg}{RESET}"

    # INFO => no change
    return msg
