import type { StructureDataDto } from '@/entities/structure/structure.dto';







// ====================================================
// Domain Models (Frontend Consumable Types) - Camel Case
// ====================================================

// ====================================================
// 히스토그램이나 막대 차트 데이터의 기본 단위
// ====================================================
export type ChartBucketItem = {
  range: string;
  count: number;
};

// ====================================================
// Structure 탭에서 최종적으로 사용할 데이터 모델
// DTO의 metrics 필드를 바로 사용
// ====================================================
export type StructureStats = {
  summaryInfo: StructureDataDto['summary_info'];
  metrics: StructureDataDto['metrics'];

  // 프론트엔드 차트 컴포넌트에서 사용하기 쉽도록 배열로 변환된 데이터
  descriptionLengthData: ChartBucketItem[];
  constraintsCountData: ChartBucketItem[];
  exampleCountData: ChartBucketItem[];
  testCaseCountData: ChartBucketItem[];
};
