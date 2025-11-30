import type {
  RawStatsSummary,
  StatsSummary,
  DifficultyDistribution,
} from './types';

const toDifficulty = (
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

const toStats = (raw: RawStatsSummary): StatsSummary => {
  const { overview, metrics } = raw;

  return {
    overview: {
      totalQuestions: overview.total_questions,
      distinctDifficulties: overview.distinct_difficulties,
      earliestCreatedAt: overview.earliest_created_at,
      latestCreatedAt: overview.latest_created_at,
      daysSpan: overview.days_span,
    },
    metrics: metrics,
    difficultyDistribution: toDifficulty(
        metrics.difficulty_distribution,
    ),
    problemsPerDay: metrics.problems_per_day,
    difficultyOverTime: metrics.difficulty_over_time.map((item) => ({
      date: item.date,
      Easy: item.Easy || 0,
      Medium: item.Medium || 0,
      Hard: item.Hard || 0,
    })),
    inputTypeDistribution: metrics.input_type_distribution,
    topTagsDistribution: metrics.top_tags_distribution,
    duplicateTitleCount: metrics.duplicate_title_count,
  };
};

export const mapper = {
  toStats,
  toDifficulty,
}