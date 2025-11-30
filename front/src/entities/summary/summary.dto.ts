// ====================================================
// DTO (Data Transfer Object) 그룹
// 백엔드에서 오는 JSON 원본 데이터의 형태를 1:1로 복사하여 정의
// 공통 타입 (다른 엔티티 DTO들이 import하여 사용)
// ====================================================

// ====================================================
// 모든 분할 JSON 파일의 최상단에 포함되는 공통 메타 정보
// generated_at은 백엔드에서 내려주는 타임스탬프
// total_records은 Overview 파일 등에 있을 수 있는 총 레코드 수
// ====================================================
export type SummaryInfo = {
  generated_at: string;
  total_records?: number;
};

export type DifficultyKeyDto = 'Easy' | 'Medium' | 'Hard';

export type DifficultyDistributionDto = {
  counts: Record<DifficultyKeyDto, number>;
  percentages: Record<DifficultyKeyDto, number>;
};

export type DistributionDto = {
  counts: Record<string, number>;
  percentages: Record<string, number>;
};

export type OverviewDto = {
  total_questions: number;
  distinct_difficulties: number;
  earliest_created_at: string;
  latest_created_at: string;
  days_span: number;
};

export type ProblemsPerDayDto = {
  date: string;
  count: number;
};

export type DifficultyOverTimeDto = {
  date: string;
} & Record<DifficultyKeyDto, number>;

export type SummaryMetricsDto = {
  difficulty_distribution: DifficultyDistributionDto;
  avg_description_length_by_difficulty: Record<DifficultyKeyDto, number>;
  avg_test_cases_by_difficulty: Record<DifficultyKeyDto, number>;
  algorithm_category_distribution: DistributionDto;
  input_type_distribution: DistributionDto;
  top_tags_distribution: Record<string, number>;
  example_count_distribution: Record<string, number>;
  test_case_count_distribution: Record<string, number>;
  example_testcase_by_difficulty: Record<
    DifficultyKeyDto,
    { num_examples: number; num_test_cases: number }
  >;
  description_length_bucket_distribution: Record<string, number>;
  constraints_count_distribution: Record<string, number>;
  problems_per_day: ProblemsPerDayDto[];
  difficulty_over_time: DifficultyOverTimeDto[];
  output_type_distribution: DistributionDto;
  negative_one_output_problems_ratio: DistributionDto;
  difficulty_algorithm_matrix: Record<DifficultyKeyDto, Record<string, number>>;
  difficulty_input_type_matrix: Record<DifficultyKeyDto, Record<string, number>>;
  duplicate_title_count: number;
  description_template_usage: Record<string, number>;
};

export type RawStatsSummary = {
  overview: OverviewDto;
  metrics: SummaryMetricsDto;
  timestamp?: string;
};