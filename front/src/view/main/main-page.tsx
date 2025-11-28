'use client';
import type { StatsSummary } from '@/entities/summary/types';
import { DifficultyChart, buildDifficultyChartVM } from '@/features/stats/difficulty-chart';
import { InputTypeChart, buildInputTypeChartVM } from '@/features/stats/input-type-chart';
import { SummaryCards } from '@/features/stats/summary-cards/ui/summary-card';
import { TopTags, buildTopTagsVM } from '@/features/stats/top-tags';
import { TrendChart } from '@/features/stats/trend-chart';
import { buildTrendChartVM } from '@/features/stats/trend-chart/model/builders';
import { MOTION_VARIANTS } from '@/shared/lib';
import { MAIN_DASHBOARD } from '@/view/main/main.constants';
import { MainHeader } from '@/widgets';
import { format } from 'date-fns';
import { motion } from 'framer-motion';

type Props = {
  stats: StatsSummary;
};

export function MainPage({ stats }: Props) {
  const { overview, difficultyDistribution } = stats;
  const latest = format(new Date(overview.latestCreatedAt), 'yyyy-MM-dd');
  const difficultyVM = buildDifficultyChartVM(stats);
  const trendVM = buildTrendChartVM(stats);
  const inputTypeVM = buildInputTypeChartVM(stats);
  const topTagsVM = buildTopTagsVM(stats);

  return (
    <main className="mx-auto flex-1 justify-center flex max-w-6xl flex-col gap-8 px-4 py-8 md:px-8 md:py-10">
      {/* 헤더 */}
      <MainHeader
        badgeText={MAIN_DASHBOARD.BADGE_TEXT}
        title={MAIN_DASHBOARD.TITLE}
        description={MAIN_DASHBOARD.DESCRIPTION(overview.daysSpan)}
        metaLabel={MAIN_DASHBOARD.META_LABEL}
        metaValue={latest}
      />

      {/* 카드 + 그래프 */}
      <motion.section
        variants={MOTION_VARIANTS.STAGGER_CONTAINER(0.06)}
        initial="hidden"
        animate="show"
        className="flex flex-col gap-6"
      >
        {/* 상단 카드 */}
        <motion.div variants={MOTION_VARIANTS.FADEINUP(0.02)}>
          <SummaryCards stats={stats} />
        </motion.div>
        {/* 중간: 날짜별 수 + 난이도 파이 */}
        <motion.div
          variants={MOTION_VARIANTS.FADEINUP(0.04)}
          className="grid gap-6 md:grid-cols-[1.5fr_1fr]"
        >
          <TrendChart vm={trendVM} />
          <DifficultyChart vm={difficultyVM} />
        </motion.div>
        {/* 하단: 입력 타입 분포 + 상위 태그 */}
        <motion.div
          variants={MOTION_VARIANTS.FADEINUP(0.06)}
          className="grid gap-6 md:grid-cols-[1.5fr_1fr]"
        >
          <InputTypeChart vm={inputTypeVM} />
          <TopTags vm={topTagsVM} />
        </motion.div>
      </motion.section>
    </main>
  );
}
