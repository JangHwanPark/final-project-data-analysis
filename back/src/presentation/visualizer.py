from __future__ import annotations
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, Any

# Infrastructure Dependencies
from infrastructure.logging import get_logger
from infrastructure.config import CHARTS_DIR

# Domain Dependencies
from domain.entities.data_model import DatasetSummary

logger = get_logger(__name__)


class Visualizer:
  # 분석 결과(DatasetSummary)를 사용하여 통계 시각화(차트)를 생성하는 프레젠테이션 클래스.

  def __init__(self):
    self.base_path = CHARTS_DIR

    # Matplotlib/Seaborn 설정
    sns.set_theme(style="whitegrid")
    # 한글/특수문자 이슈 방지를 위해 기본 폰트 설정 (시스템 폰트 사용 가정)
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['figure.dpi'] = 100  # 기본 DPI 설정
    logger.info(f"Visualizer initialized. Charts will be saved to: {self.base_path}")

  def create_and_save_charts(self, summary: DatasetSummary):
    """
    주요 통계 지표를 시각화하여 파일로 저장합니다.

    :param summary: DatasetSummary 객체.
    """
    logger.info("Starting chart generation.")
    metrics = summary.metrics

    # 1. 난이도별 분포 (파이 차트)
    self._plot_pie_distribution(
      data=metrics['difficulty_distribution'],
      title='Distribution by Difficulty Level',
      filename='difficulty_pie_chart.png'
    )

    # 2. 상위 태그 분포 (막대 그래프)
    self._plot_bar_chart(
      data=metrics['top_tags_distribution'],
      title='Top 10 Problem Tags',
      filename='top_tags_bar_chart.png',
      x_label='Tag',
      y_label='Count'
    )

    # 3. 알고리즘 카테고리 분포 (막대 그래프)
    self._plot_bar_distribution(
      data=metrics['algorithm_category_distribution'],
      title='Algorithm Category Distribution',
      filename='algorithm_category_bar_chart.png'
    )

    logger.info("Chart generation complete.")

  def _save_figure(self, fig: plt.Figure, filename: str):
    # 그림 객체를 파일 경로에 저장하고 메모리에서 해제합니다.
    filepath = self.base_path / filename
    fig.savefig(filepath, bbox_inches='tight')
    plt.close(fig)  # 메모리 해제
    logger.info(f"SUCCESS: Chart saved to {filepath}")

  def _plot_pie_distribution(self, data: Dict[str, Dict[str, Any]], title: str, filename: str):
    # 파이 차트 생성 (비율 데이터용).
    counts = data['counts']
    labels = counts.keys()
    sizes = counts.values()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(
      sizes,
      labels=labels,
      autopct='%1.1f%%',
      startangle=90,
      textprops={'fontsize': 10, 'weight': 'bold'}
    )
    ax.axis('equal')
    ax.set_title(title, fontsize=14, fontweight='bold')
    self._save_figure(fig, filename)

  def _plot_bar_distribution(self, data: Dict[str, Dict[str, Any]], title: str, filename: str):
    # 분포 딕셔너리를 사용하여 막대 그래프 생성.
    self._plot_bar_chart(data['counts'], title, filename, x_label='Category', y_label='Count')

  def _plot_bar_chart(self, data: Dict[str, int], title: str, filename: str, x_label: str, y_label: str):
    # 일반적인 딕셔너리를 사용하여 막대 그래프 생성.
    categories = list(data.keys())
    counts = list(data.values())

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=categories, y=counts, ax=ax, palette="viridis")

    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.set_xlabel(x_label, fontsize=12)
    ax.set_ylabel(y_label, fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    self._save_figure(fig, filename)
