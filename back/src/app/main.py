from core.config import (
  ensure_directories,
  DATA_FILE,
  SUMMARIES_DIR,
)
from infrastructure.io.csv_loader import load_csv
from domain.service.metrics import compute_statistics
from infrastructure.io.artifact_writer import write_json
from infrastructure.logging import get_logger
from infrastructure.logging.steps import StepLogger


def main():
  logger = get_logger("main")
  steps = StepLogger(total_steps=4, logger_name="main")

  try:
    logger.info("=== Data Analysis Pipeline Started ===")
    # artifacts 디렉토리 준비
    steps.step("Ensuring directories...")
    ensure_directories()

    # 데이터 로드(Load CSV)
    steps.step(f"Loading CSV: {DATA_FILE}")
    df = load_csv(DATA_FILE)

    # 통계 계산(Compute statistics)
    steps.step("Computing metrics...")
    summary = compute_statistics(df)

    # 저장 경로 설정 & JSON 파일로 저장(Export as JSON file)
    output_path = SUMMARIES_DIR / "summary.json"
    steps.step(f"Writing summary to {output_path}")
    write_json(summary, output_path)
    logger.info("=== Analysis Complete. Artifacts saved to ./artifacts ===")
  except Exception as e:
    logger.exception("Pipeline failed due to an unexpected error.")
    logger.error("Pipeline failed.")
  finally:
    logger.info("=== Pipeline Finished ===")


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
  main()
