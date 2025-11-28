import type { StatsSummary } from '@/entities/summary/types';
import type { TrendChartVM } from './types';

export const buildTrendChartVM = (stats: StatsSummary): TrendChartVM => {
  const { overview, problemsPerDay } = stats;

  return {
    title: '날짜별 문제 수',
    rightLabel: `총 ${overview.totalQuestions.toLocaleString('ko-KR')}문제`,
    points: problemsPerDay,
  };
}