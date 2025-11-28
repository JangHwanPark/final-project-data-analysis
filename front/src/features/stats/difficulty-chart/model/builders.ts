import type { StatsSummary, DifficultyKey } from '@/entities/summary/types';
import type { DifficultyChartVM, DifficultyChartItem } from './types';

export const buildDifficultyChartVM = (stats: StatsSummary): DifficultyChartVM => {
  const { difficultyDistribution } = stats;

  const keys = Object.keys(
    difficultyDistribution.counts,
  ) as DifficultyKey[];

  const items: DifficultyChartItem[] = keys
    .map((key) => ({
      key,
      label: key,
      count: difficultyDistribution.counts[key],
      percentage: difficultyDistribution.percentages[key],
    }))
    // 많이 등장한 순으로 정렬 (기존 로직 유지)
    .sort((a, b) => b.count - a.count);

  return {
    title: '난이도 분포',
    rightLabel: 'Hard / Medium / Easy 비율',
    items,
  };
};
