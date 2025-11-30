from __future__ import annotations

import argparse
from pathlib import Path

from app.pipeline_options import PipelineOptions, default_frontend_targets
from app_types.pipelien import AnalysisScope
from constants.cli import (
  CLI_DESCRIPTION,
  CLI_EPILOG,
  ENGINE_CHOICES,
  ENGINE_DEFAULT,
  DEFAULT_DATA_FILE,
)
from constants.path import ArtifactsPaths


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

  return parser


def parse_arguments() -> tuple[PipelineOptions, bool]:
  parser = build_parser()
  args = parser.parse_args()

  # 비대화형 모드(--no-interactive)일 때 사용할 기본 옵션 및 경로 설정
  options = PipelineOptions(
    data_file=args.data_file,
    engine=args.engine,
    analysis_scope=AnalysisScope.FULL,
    output_targets={"json", "excel", "charts"},
    json_dir=ArtifactsPaths.JSON,
    charts_dir=ArtifactsPaths.CHARTS,
    xlsx_dir=ArtifactsPaths.XLSX,
    frontend_json_targets=default_frontend_targets(analysis_scope=AnalysisScope.FULL),
  )

  interactive = not args.no_interactive
  return options, interactive
