import logging
from infrastructure.logging import get_logger
from infrastructure.logging.style import FG, STYLE, colorize
from wcwidth import wcswidth

# 배너 전용 로거
logger = get_logger("banner")
_SIMPLE_FORMAT = "%(message)s"

for handler in logger.handlers:
  handler.setFormatter(logging.Formatter(_SIMPLE_FORMAT))


def _display_center(text: str, width: int) -> str:
  # 실제 표시 폭
  disp_len = wcswidth(text)
  if disp_len >= width:
    return text

  pad_total = width - disp_len
  left = pad_total // 2
  right = pad_total - left
  return " " * left + text + " " * right


# ====================================================
# 여러 줄의 텍스트를 width 기준으로
# 가운데 정렬 + 색상(굵기) 적용하여 리스트로 반환
# ====================================================
def _format_center_lines(
        text: str,
        width: int,
        color: str | None,
        bold: bool
):
  lines = []
  for part in text.split("\n"):
    centered = _display_center(part, width)
    if color:
      centered = colorize(centered, STYLE.BOLD, color) if bold else colorize(centered, color)
    lines.append(centered)
  return lines


def log_banner(
        title: str,
        width: int = 84,
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
  line_colored = colorize(line, line_color) if line_color else line

  # Multi-line formatting
  formatted_lines = _format_center_lines(title, width, color, bold)

  # 출력
  logger.info(line_colored)
  for fl in formatted_lines:
    logger.info(fl)
  logger.info(line_colored)

  if newline_after:
    logger.info("")
