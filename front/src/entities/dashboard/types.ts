// ====================================================
// 공통 타입
// ====================================================

/** 난이도 키 (Easy, Medium, Hard) */
export type DifficultyKey = 'Easy' | 'Medium' | 'Hard';

/** 카운트 및 퍼센티지 분포를 나타내는 공통 구조 */
export type Distribution = {
  counts: Record<string, number>;
  percentages: Record<string, number>;
};

/** 모든 분할 JSON 파일의 최상단에 포함되는 메타 정보 */
export type SummaryInfo = {
  generated_at: string;
  total_records?: number; // Overview 파일에 있을 수 있는 총 레코드 수
};

// ====================================================
// 1. Difficulty & Volume (difficulty.json)
// ====================================================

export type DailyDifficultyTrend = {
  date: string;
} & Record<DifficultyKey, number>; // Easy, Medium, Hard 필드 포함

export type AvgComplexity = {
  Easy: number;
  Medium: number;
  Hard: number;
};

export type DifficultyData = {
  summary_info: SummaryInfo;
  metrics: {
    difficulty_distribution: Distribution;
    difficulty_over_time: DailyDifficultyTrend[];
    avg_description_length_by_difficulty: AvgComplexity;
    avg_test_cases_by_difficulty: AvgComplexity;
  };
};

// ====================================================
// 2. Structure (structure.json)
// ====================================================

export type BucketDistribution = Record<string, number>;

export type StructureData = {
  summary_info: SummaryInfo;
  metrics: {
    description_length_bucket_distribution: BucketDistribution;
    constraints_count_distribution: BucketDistribution;
    example_count_distribution: BucketDistribution;
    test_case_count_distribution: BucketDistribution;
  };
};

// ====================================================
// 3. RawData (summary-full.json) - 전체 구조를 포함하는 타입
// (전체 RawStatsSummary와 유사하나, 프론트엔드 포맷에 맞춤)
// ====================================================

// [주의] RawData는 모든 메트릭을 포함하는 가장 큰 타입입니다.
// RawDataContent 컴포넌트에서 사용될 수 있습니다.
export type RawData = {
  summary_info: SummaryInfo;
  // 모든 metrics가 포함되므로 any로 처리하거나 백엔드 원본 타입과 연결해야 함
  metrics: any;
};
