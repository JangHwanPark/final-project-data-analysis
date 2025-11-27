from app.config import ensure_directories, DATA_FILE
from infrastructure.io.csv_loader import load_csv
from domain.service.metrics import compute_statistics
from infrastructure.io.artifact_writer import write_json

def main():
  print("=== Data Analysis Pipeline Started ===")
  ensure_directories()
  # Load CSV
  df = load_csv(DATA_FILE)
  # Compute statistics
  summary = compute_statistics(df)
  # Export as JSON file
  write_json(summary, "summary.json")
  print("=== Analysis Complete. Artifacts saved to ./artifacts ===")


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
  main()
