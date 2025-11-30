import type { SummaryMetricsDto, DistributionDto, SummaryInfo } from '@/entities/summary';

// ====================================================
// 백엔드에서 내려오는 tags.json 파일의 스펙을 정의
// SummaryMetricsDto 중 Tags 관련 필드만 포함
// ====================================================
export type TagsMetricsDto = Pick<
  SummaryMetricsDto,
  | 'top_tags_distribution'
  | 'algorithm_category_distribution'
  | 'input_type_distribution'
>;

// ====================================================
// Tags 탭의 원본 JSON 파일 구조
// ====================================================
export type TagsDataDto = {
  summary_info: SummaryInfo;
  metrics: TagsMetricsDto;
};