import type { SummaryInfo, SummaryMetricsDto } from '@/entities/summary';

// ====================================================
// 백엔드에서 내려오는 structure.json 파일의 스펙을 정의
// (SummaryMetricsDto 중 Structure 관련 필드만 포함)
// ====================================================
export type StructureMetricsDto = Pick<
  SummaryMetricsDto,
  | 'description_length_bucket_distribution'
  | 'constraints_count_distribution'
  | 'example_count_distribution'
  | 'test_case_count_distribution'
>;

// ====================================================
// Structure 탭의 원본 JSON 파일 구조입니다.
// ====================================================
export type StructureDataDto = {
  summary_info: SummaryInfo;
  metrics: StructureMetricsDto;
};
