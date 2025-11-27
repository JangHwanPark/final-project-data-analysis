import logging
from typing import Optional
from infrastructure.logging.color_formatter import ColorFormatter

_DEFAULT_FORMAT = "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
_DEFAULT_LEVEL = logging.INFO


def get_logger(name: Optional[str] = None) -> logging.Logger:
  """
  주어진 이름에 대해 설정된 로거 인스턴스를 반환합니다.

  이 로거는 스트림 핸들러(콘솔 출력)를 사용하여 이름별로 단 한 번만 설정됩니다.
  파이프라인 단계별 디버깅 추적을 쉽게 하기 위해 간단하고 타임스탬프가 포함된 형식을 사용합니다.

  :param name: 로거의 이름 (예: 'data_loader', 'analysis_service'). None이면 루트 로거를 반환합니다.
  :return: 구성이 완료된 logging.Logger 인스턴스.
  """
  logger = logging.getLogger(name)
  if not logger.handlers:
    # 로거 레벨 설정
    logger.setLevel(_DEFAULT_LEVEL)
    # 스트림 핸들러 생성(콘솔/터미널 출력 담당)
    handler = logging.StreamHandler()

    # [포맷 설정] 기본 로그는 ColorFormatter 사용
    handler.setFormatter(ColorFormatter(_DEFAULT_FORMAT))
    # 로거내 핸들러 추가
    logger.addHandler(handler)
    # 로그 전파 방지(부모 로거로 전파되는 것 방지)
    logger.propagate = False
  return logger
