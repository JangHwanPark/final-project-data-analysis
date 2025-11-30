import type { TagsDataDto } from '@/entities/tags/tags.dto';
import type { DistributionDto } from '@/entities/summary';

// ====================================================
// Domain Models (Frontend Consumable Types) - Camel Case
// ====================================================

// ====================================================
// Top Tags 차트용 데이터 (배열로 변환)
// ====================================================
export type TopTagItem = {
  name: string;
  count: number;
};

// ====================================================
// Tags 탭에서 최종적으로 사용할 데이터 모델
// ====================================================
export type TagsStats = {
  summaryInfo: TagsDataDto['summary_info'];
  metrics: TagsDataDto['metrics'];
  
  // 가공된 데이터 (가장 많이 쓰이는 데이터는 별도 속성으로 분리)
  topTagsList: TopTagItem[];
  algorithmCategoryDistribution: DistributionDto;
  inputTypeDistribution: DistributionDto;
};