import { DifficultyDataDto } from '@/entities/difficulty/difficulty.dto';
import { ComplexityMetric, DifficultyStats } from '@/entities/difficulty/types';

/**
 * 백엔드에서 받은 Raw Difficulty DTO를 프론트엔드용 DifficultyStats로 매핑합니다.
 * @param raw DifficultyDataDto (difficulty.json)
 * @returns DifficultyStats (프론트엔드 사용 모델)
 */
const toDifficultyStats = (raw: DifficultyDataDto): DifficultyStats => {
  const { summary_info, metrics } = raw;

  // Complexity Chart용 데이터 매핑 함수
  const mapComplexityData = (m: DifficultyDataDto['metrics']): ComplexityMetric[] => {
    return (['Easy', 'Medium', 'Hard'] as const).map((key) => ({
      name: key,
      descLength: m.avg_description_length_by_difficulty[key] || 0,
      testCases: m.avg_test_cases_by_difficulty[key] || 0,
    }));
  };

  return {
    summaryInfo: summary_info,
    metrics: metrics, // 원본 metrics 유지

    // 주요 지표는 그대로 사용
    difficultyDistribution: metrics.difficulty_distribution,
    difficultyOverTime: metrics.difficulty_over_time,

    // 차트 컴포넌트에서 바로 사용할 수 있도록 가공
    complexityData: mapComplexityData(metrics),
  };
};

export const mapper = {
  toDifficultyStats,
};
