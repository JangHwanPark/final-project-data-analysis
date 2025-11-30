import { TagsDataDto } from '@/entities/tags/tags.dto';
import { TagsStats, TopTagItem } from '@/entities/tags/types';

/**
 * 백엔드에서 받은 Raw Tags DTO를 프론트엔드용 TagsStats로 매핑합니다.
 * @param raw TagsDataDto (tags.json)
 * @returns TagsStats (프론트엔드 사용 모델)
 */
const toTagsStats = (raw: TagsDataDto): TagsStats => {
  const { summary_info, metrics } = raw;

  // Object 형태의 top_tags_distribution을 배열로 변환하는 헬퍼 함수
  const mapTopTagsToArray = (data: Record<string, number>): TopTagItem[] => {
    return (
      Object.entries(data)
        .map(([name, count]) => ({
          name: name,
          count: count,
        }))
        // 카운트가 높은 순서로 정렬
        .sort((a, b) => b.count - a.count)
    );
  };

  return {
    summaryInfo: summary_info,
    metrics: metrics, // 원본 metrics 유지

    // 차트 컴포넌트에서 바로 사용할 수 있도록 데이터 가공
    topTagsList: mapTopTagsToArray(metrics.top_tags_distribution),
    algorithmCategoryDistribution: metrics.algorithm_category_distribution,
    inputTypeDistribution: metrics.input_type_distribution,
  };
};

export const mapper = {
  toTagsStats,
};
