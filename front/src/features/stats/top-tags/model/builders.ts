import type { StatsSummary } from '@/entities/summary/types';
import type { TopTagsVM } from '@/features/stats/top-tags';

const DEFAULT_TOP_N = 5;

/** StatsSummary → TopTagsVM */
export const buildTopTagsVM = (
  stats: StatsSummary,
  topN: number = DEFAULT_TOP_N,
): TopTagsVM => {
  const { topTagsDistribution } = stats;

  const sorted = Object.entries(topTagsDistribution)
    .sort((a, b) => b[1] - a[1])
    .slice(0, topN);

  const items = sorted.map(([tag, count], index) => ({
    rank: index + 1,
    tag,
    count,
  }));

  return { items };
}