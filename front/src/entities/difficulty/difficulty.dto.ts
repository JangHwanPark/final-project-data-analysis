import type { SummaryInfo, SummaryMetricsDto } from '@/entities/summary';





// ====================================================
// 백엔드에서 내려오는 difficulty.json 파일의 스펙을 정의
// SummaryMetricsDto 중 Difficulty 관련 필드만 포함
// ====================================================
export type DifficultyMetricsDto = Pick<
  SummaryMetricsDto,
  | 'difficulty_distribution'
  | 'difficulty_over_time'
  | 'avg_description_length_by_difficulty'
  | 'avg_test_cases_by_difficulty'
>;

// ====================================================
// Difficulty 탭의 원본 JSON 파일 구조
// ====================================================
export type DifficultyDataDto = {
  summary_info: SummaryInfo;
  metrics: DifficultyMetricsDto;
};
