export type RawStatsSummary = {
  overview: {
    total_questions: number;
    distinct_difficulties: number;
    earliest_created_at: string;
    latest_created_at: string;
    days_span: number;
  };
  metrics: {
    difficulty_distribution: {
      counts: {
        Hard: number;
        Medium: number;
        Easy: number;
      };
      percentages: {
        Hard: number;
        Medium: number;
        Easy: number;
      };
    };
    avg_description_length_by_difficulty: Record<string, number>;
    avg_test_cases_by_difficulty: Record<string, number>;
    algorithm_category_distribution: {
      counts: Record<string, number>;
      percentages: Record<string, number>;
    };
    input_type_distribution: {
      counts: Record<string, number>;
      percentages: Record<string, number>;
    };
    top_tags_distribution: Record<string, number>;
    example_count_distribution: Record<string, number>;
    test_case_count_distribution: Record<string, number>;
    example_testcase_by_difficulty: {
      Easy: { num_examples: number; num_test_cases: number };
      Hard: { num_examples: number; num_test_cases: number };
      Medium: { num_examples: number; num_test_cases: number };
    };
    description_length_bucket_distribution: Record<string, number>;
    constraints_count_distribution: Record<string, number>;
    problems_per_day: {
      date: string;
      count: number;
    }[];
    difficulty_over_time: {
      date: string;
      Easy: number;
      Hard: number;
      Medium: number;
    }[];
    output_type_distribution: {
      counts: Record<string, number>;
      percentages: Record<string, number>;
    };
    negative_one_output_problems_ratio: {
      counts: Record<string, number>;
      percentages: Record<string, number>;
    };
    difficulty_algorithm_matrix: Record<string, Record<string, number>>;
    difficulty_input_type_matrix: Record<string, Record<string, number>>;
    duplicate_title_count: number;
    description_template_usage: Record<string, number>;
  };
};

// 메인 페이지에서 쓸 도메인 모델
export type DifficultyKey = 'Easy' | 'Medium' | 'Hard';

export type Overview = {
  totalQuestions: number;
  distinctDifficulties: number;
  earliestCreatedAt: string;
  latestCreatedAt: string;
  daysSpan: number;
};

export type DifficultyDistribution = {
  counts: Record<DifficultyKey, number>;
  percentages: Record<DifficultyKey, number>;
};

export type ProblemsPerDayItem = {
  date: string;
  count: number;
};

export type DifficultyOverTimeItem = {
  date: string;
} & Record<DifficultyKey, number>;

export type InputTypeDistribution = {
  counts: Record<string, number>;
  percentages: Record<string, number>;
};

export type TopTagsDistribution = Record<string, number>;

export type StatsSummary = {
  overview: Overview;
  difficultyDistribution: DifficultyDistribution;
  problemsPerDay: ProblemsPerDayItem[];
  difficultyOverTime: DifficultyOverTimeItem[];
  inputTypeDistribution: InputTypeDistribution;
  topTagsDistribution: TopTagsDistribution;
  duplicateTitleCount: number;

  // dumy
  metrics: RawStatsSummary['metrics'];
};
