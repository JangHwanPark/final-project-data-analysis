import type {StatsSummary} from "@/entities/summary/types";
import {format} from "date-fns";
import {SummaryCardVM} from "@/features/stats/summary-cards/model";

export function buildSummaryCards(stats: StatsSummary): SummaryCardVM[] {
  const { overview, difficultyDistribution, duplicateTitleCount } = stats;

  const earliest = format(new Date(overview.earliestCreatedAt), 'yyyy-MM-dd');
  const latest = format(new Date(overview.latestCreatedAt), 'yyyy-MM-dd');

  return [
    {
      id: 'total',
      label: '총 문제 수',
      value: overview.totalQuestions.toLocaleString('ko-KR'),
      subLabel: `${earliest} ~ ${latest} (${overview.daysSpan}일)`,
    },
    {
      id: 'difficulty',
      label: '난이도 분포',
      value: `${difficultyDistribution.counts.Hard}H / ${difficultyDistribution.counts.Medium}M / ${difficultyDistribution.counts.Easy}E`,
      subLabel: 'Hard / Medium / Easy',
    },
    {
      id: 'duplicates',
      label: '중복 제목 수',
      value: duplicateTitleCount.toString(),
      subLabel: '비슷한 유형의 문제들',
    },
  ];
}
