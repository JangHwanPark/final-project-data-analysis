import type { StatsSummary } from '@/entities/summary/types';
import type { InputTypeChartVM } from '@/features/stats/input-type-chart';

/**
 * StatsSummary → InputTypeChartVM<br/>
 * API 응답 구조가 바뀌어도 여기만 고치면 됨.
 */
export const buildInputTypeChartVM = (stats: StatsSummary): InputTypeChartVM => {
  const { inputTypeDistribution } = stats;

  const items = Object.entries(inputTypeDistribution.percentages).map(
    ([name, value]) => ({
      name,
      value,
    }),
  );

  return { items };
}
