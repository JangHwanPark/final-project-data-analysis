from __future__ import annotations

import argparse
from pathlib import Path

from app.pipeline_options import PipelineOptions
from constants.cli import (
  CLI_DESCRIPTION,
  CLI_EPILOG,
  ENGINE_CHOICES,
  ENGINE_DEFAULT,
  DEFAULT_DATA_FILE,
)


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(
    description=CLI_DESCRIPTION,
    epilog=CLI_EPILOG,
  )

  parser.add_argument(
    "--data-file",
    type=Path,
    default=DEFAULT_DATA_FILE,
    help="분석할 CSV 파일의 경로를 지정합니다.",
  )

  parser.add_argument(
    "--engine",
    type=str,
    default=ENGINE_DEFAULT,
    choices=ENGINE_CHOICES,
    help="데이터 로딩 엔진 선택(csv, json, db)",
  )

  parser.add_argument(
    "--no-interactive",
    action="store_true",
    help="인터랙티브 모드를 끄고 기본 옵션으로 실행합니다.",
  )

  # 나중에 --no-charts, --no-excel 추가하면 여기서 확장

  return parser


def parse_arguments() -> tuple[PipelineOptions, bool]:
  parser = build_parser()
  args = parser.parse_args()

  options = PipelineOptions(
    data_file=args.data_file,
    generate_charts=True,
    generate_excel=True,
    engine=args.engine,
    analysis_scope="full",
    output_targets={"json", "excel", "charts"},
  )

  interactive = not args.no_interactive
  return options, interactive
