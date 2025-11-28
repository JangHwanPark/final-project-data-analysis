import type {
  RawStatsSummary,
  StatsSummary,
  DifficultyDistribution,
  DifficultyKey,
} from './types';

export const mapDifficultyDistribution = (
    src: RawStatsSummary['metrics']['difficulty_distribution'],
): DifficultyDistribution => ({
  counts: {
    Easy: src.counts.Easy,
    Medium: src.counts.Medium,
    Hard: src.counts.Hard,
  },
  percentages: {
    Easy: src.percentages.Easy,
    Medium: src.percentages.Medium,
    Hard: src.percentages.Hard,
  },
});

export const mapStatsSummary = (raw: RawStatsSummary): StatsSummary => {
  const { overview, metrics } = raw;

  return {
    overview: {
      totalQuestions: overview.total_questions,
      distinctDifficulties: overview.distinct_difficulties,
      earliestCreatedAt: overview.earliest_created_at,
      latestCreatedAt: overview.latest_created_at,
      daysSpan: overview.days_span,
    },
    difficultyDistribution: mapDifficultyDistribution(
        metrics.difficulty_distribution,
    ),
    problemsPerDay: metrics.problems_per_day,
    difficultyOverTime: metrics.difficulty_over_time.map((item) => ({
      date: item.date,
      Easy: item.Easy,
      Medium: item.Medium,
      Hard: item.Hard,
    })),
    inputTypeDistribution: metrics.input_type_distribution,
    topTagsDistribution: metrics.top_tags_distribution,
    duplicateTitleCount: metrics.duplicate_title_count,
  };
};
