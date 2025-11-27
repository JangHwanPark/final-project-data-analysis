RESET = "\033[0m"


class FG:
  BLACK = "\033[30m"
  RED = "\033[31m"
  GREEN = "\033[32m"
  YELLOW = "\033[33m"
  BLUE = "\033[34m"
  MAGENTA = "\033[35m"
  CYAN = "\033[36m"
  WHITE = "\033[37m"


class BG:
  BLACK = "\033[40m"
  RED = "\033[41m"
  GREEN = "\033[42m"
  YELLOW = "\033[43m"
  BLUE = "\033[44m"
  MAGENTA = "\033[45m"
  CYAN = "\033[46m"
  WHITE = "\033[47m"


class STYLE:
  BOLD = "\033[1m"
  DIM = "\033[2m"
  ITALIC = "\033[3m"
  UNDERLINE = "\033[4m"


def colorize(text: str, *codes: str) -> str:
  # text에 ANSI 스타일(색상, 볼드 등)을 적용해 반환.
  # codes → FG.RED, BG.BLUE, STYLE.BOLD 등 조합 가능.
  return "".join(codes) + text + RESET
