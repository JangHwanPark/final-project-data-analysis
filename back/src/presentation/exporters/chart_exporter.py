from __future__ import annotations

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path
from typing import Optional, Any, Dict

# Infrastructure Dependencies
from infrastructure.logging import get_logger

# Domain Dependencies
from domain.entities.data_model import DatasetSummary

logger = get_logger(__name__)


# ====================================================
# DatasetSummary(분석 결과)를 시각화하여 차트 이미지 파일로 내보내는 클래스.
# ====================================================
class ChartExporter:
  def __init__(self):
    sns.set_theme(style="whitegrid")
    logger.info("ChartExporter initialized.")

  def export(self, summary: DatasetSummary, output_dir: Path) -> None:
    """
    분석 결과를 시각화하여 지정된 디렉토리에 이미지 파일로 저장합니다.

    :param summary: 도메인 데이터 객체 (DatasetSummary)
    :param output_dir: 이미지를 저장할 디렉토리 경로
    """
    logger.info(f"Attempting to export charts to {output_dir}")

    # 1. 데이터 컨텍스트 추출
    metrics = self._extract_metrics(summary)
    if not metrics:
      return

    try:
      # 2. 출력 디렉토리 생성
      output_dir.mkdir(parents=True, exist_ok=True)

      # 3. 차트 생성 작업 수행
      self._plot_difficulty_distribution(metrics, output_dir)
      self._plot_algorithm_distribution(metrics, output_dir)
      self._plot_top_tags(metrics, output_dir)
      self._plot_difficulty_averages(metrics, output_dir)

      logger.info(f"SUCCESS: Charts exported to {output_dir}")

    except Exception as e:
      logger.exception(f"ERROR: Failed to export charts to {output_dir}")

  # ====================================================
  # Private Helper Methods
  # DatasetSummary에서 metrics 딕셔너리를 추출
  # ====================================================
  def _extract_metrics(self, summary: DatasetSummary | dict) -> Optional[Dict[str, Any]]:
    try:
      if hasattr(summary, "to_dict"):
        return summary.to_dict().get("metrics", {})
      elif isinstance(summary, dict):
        return summary.get("metrics", {})
      return None
    except Exception:
      logger.warning("Failed to extract metrics for charting.")
      return None

  # ====================================================
  # [차트 1] 난이도 분포 막대 그래프
  # ====================================================
  def _plot_difficulty_distribution(self, metrics: Dict[str, Any], output_dir: Path):
    data = metrics.get("difficulty_distribution", {}).get("counts", {})
    if not data:
      return

    plt.figure(figsize=(10, 6))
    df = pd.Series(data).sort_values(ascending=False).to_frame(name="Count")

    sns.barplot(x=df.index, y="Count", data=df, palette="viridis", hue=df.index, legend=False)
    plt.title("Problem Count by Difficulty Level")
    plt.xlabel("Difficulty")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()

    save_path = output_dir / "difficulty_distribution.png"
    plt.savefig(save_path)
    plt.close()

  # ====================================================
  # [차트 2] 알고리즘 카테고리 분포 막대 그래프
  # ====================================================
  def _plot_algorithm_distribution(self, metrics: Dict[str, Any], output_dir: Path):
    data = metrics.get("algorithm_category_distribution", {}).get("counts", {})
    if not data:
      return

    plt.figure(figsize=(12, 6))
    df = pd.Series(data).sort_values(ascending=False).head(15).to_frame(name="Count")

    sns.barplot(x="Count", y=df.index, data=df, palette="rocket", hue=df.index, legend=False)
    plt.title("Top Algorithm Categories")
    plt.xlabel("Count")
    plt.ylabel("Category")
    plt.tight_layout()

    save_path = output_dir / "algorithm_distribution.png"
    plt.savefig(save_path)
    plt.close()

  # ====================================================
  # [차트 3] 상위 태그 분포 그래프
  # ====================================================
  def _plot_top_tags(self, metrics: Dict[str, Any], output_dir: Path):
    data = metrics.get("top_tags_distribution", {})
    if not data:
      return

    plt.figure(figsize=(12, 6))
    df = pd.Series(data).sort_values(ascending=False).head(15).to_frame(name="Count")

    sns.barplot(x="Count", y=df.index, data=df, palette="mako", hue=df.index, legend=False)
    plt.title("Top 15 Problem Tags")
    plt.xlabel("Frequency")
    plt.ylabel("Tag")
    plt.tight_layout()

    save_path = output_dir / "top_tags.png"
    plt.savefig(save_path)
    plt.close()

  # ====================================================
  # [차트 4] 난이도별 평균 설명 길이 & 테스트 케이스 수 (이중 축)
  # ====================================================
  def _plot_difficulty_averages(self, metrics: Dict[str, Any], output_dir: Path):
    avg_desc = metrics.get("avg_description_length_by_difficulty", {})
    avg_test = metrics.get("avg_test_cases_by_difficulty", {})

    if not avg_desc or not avg_test:
      return

    df_desc = pd.Series(avg_desc).to_frame(name="Description Length")
    df_test = pd.Series(avg_test).to_frame(name="Test Cases")
    df = pd.concat([df_desc, df_test], axis=1).sort_index()

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # 축 1: 설명 길이 (Bar)
    sns.barplot(x=df.index, y="Description Length", data=df, ax=ax1, color="skyblue", alpha=0.6)
    ax1.set_ylabel("Avg Description Length", color="blue")
    ax1.tick_params(axis='y', labelcolor="blue")
    ax1.set_title("Averages by Difficulty: Description Length vs Test Cases")

    # 축 2: 테스트 케이스 수 (Line)
    ax2 = ax1.twinx()
    sns.lineplot(x=df.index, y="Test Cases", data=df, ax=ax2, color="red", marker="o", linewidth=2)
    ax2.set_ylabel("Avg Test Case Count", color="red")
    ax2.tick_params(axis='y', labelcolor="red")

    plt.tight_layout()
    save_path = output_dir / "difficulty_averages.png"
    plt.savefig(save_path)
    plt.close()
