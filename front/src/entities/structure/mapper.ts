import type { StructureDataDto } from '@/entities/structure/structure.dto';
import { ChartBucketItem, StructureStats } from '@/entities/structure/types';

/**
 * 백엔드에서 받은 Raw Structure DTO를 프론트엔드용 StructureStats로 매핑합니다.
 * @param raw StructureDataDto (structure.json)
 * @returns StructureStats (프론트엔드 사용 모델)
 */
const toStructureStats = (raw: StructureDataDto): StructureStats => {
  const { summary_info, metrics } = raw;

  // Object 형태의 분포 데이터를 Recharts용 배열 형태로 변환하는 헬퍼 함수
  const mapToChartBuckets = (data: Record<string, number>): ChartBucketItem[] => {
    return Object.entries(data).map(([range, count]) => ({
      range: range,
      count: count,
    }));
  };

  return {
    summaryInfo: summary_info,
    metrics: metrics, // 원본 metrics 유지

    // 차트 컴포넌트에서 바로 사용할 수 있도록 데이터 가공
    descriptionLengthData: mapToChartBuckets(metrics.description_length_bucket_distribution),
    constraintsCountData: mapToChartBuckets(metrics.constraints_count_distribution),
    exampleCountData: mapToChartBuckets(metrics.example_count_distribution),
    testCaseCountData: mapToChartBuckets(metrics.test_case_count_distribution),
  };
};

export const mapper = {
  toStructureStats,
};
