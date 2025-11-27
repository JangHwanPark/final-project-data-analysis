import logging
from infrastructure.logging import get_logger
from infrastructure.logging.style import FG, STYLE, colorize

 # 배너 전용 로거
logger = get_logger("banner")
_SIMPLE_FORMAT = "%(message)s"

for handler in logger.handlers:
    handler.setFormatter(logging.Formatter(_SIMPLE_FORMAT))

def log_banner(
        title: str,
        width: int = 200,
        color: str | None = FG.CYAN,
        line_color: str | None = FG.BLUE,
        bold: bool = True,
        newline_after: bool = True,
        newline_before: bool = True,
) -> None:
  """
  스타일 배너 출력:
    - 라인 색 변경
    - 타이틀 색 변경
    - 배너 끝에 줄바꿈 옵션

  :param title: 배너 타이틀 텍스트
  :param width: 배너 가로폭
  :param color: 타이틀 색상
  :param line_color: 라인 색상
  :param bold: 타이틀 bold 처리 여부
  :param newline_after: 배너 뒤에 한 줄 띄울지 여부
  :param newline_before: 배너 앞에 한 줄 띄울지 여부
  """
  if newline_before:
    logger.info("")

  line = "=" * width

  # Line 컬러
  if line_color:
    line_colored = colorize(line, line_color)
  else:
    line_colored = line

  # Title 컬러 + Bold 옵션
  title_text = title.center(width)
  if color:
    if bold:
      title_text = colorize(title_text, STYLE.BOLD, color)
    else:
      title_text = colorize(title_text, color)

  # 출력
  logger.info(line_colored)
  logger.info(title_text)
  logger.info(line_colored)

  if newline_after:
    logger.info("")
