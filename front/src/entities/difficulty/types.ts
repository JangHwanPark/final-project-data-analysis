import type { DifficultyDataDto } from '@/entities/difficulty/difficulty.dto';
import type {
  DifficultyDistributionDto,
  DifficultyKeyDto,
  DifficultyOverTimeDto,
  SummaryInfo,
} from '@/entities/summary';

// ====================================================
// Domain Models (Frontend Consumable Types) - Camel Case
// ====================================================

// ====================================================
// 차트에서 사용할 복잡도 비교 데이터 단위
// ====================================================
export type ComplexityMetric = {
  name: DifficultyKeyDto;
  descLength: number;
  testCases: number;
};

// ====================================================
// Difficulty 탭에서 최종적으로 사용할 데이터 모델
// ====================================================
export type DifficultyStats = {
  summaryInfo: SummaryInfo;
  metrics: DifficultyDataDto['metrics'];

  // 가공된 데이터 (컴포넌트에서 바로 사용할 수 있도록 변환)
  difficultyDistribution: DifficultyDistributionDto; // 그대로 사용
  difficultyOverTime: DifficultyOverTimeDto[]; // 그대로 사용
  complexityData: ComplexityMetric[]; // 차트 컴포넌트용으로 변환
};
