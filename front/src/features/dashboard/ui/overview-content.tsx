import React from 'react';
import { motion } from 'framer-motion';

import type { StatsSummary } from '@/entities/summary/types';
import { DifficultyChart, buildDifficultyChartVM } from '@/features/stats/difficulty-chart';
import { InputTypeChart, buildInputTypeChartVM } from '@/features/stats/input-type-chart';
import { SummaryCards } from '@/features/stats/summary-cards/ui/summary-card';
import { TopTags, buildTopTagsVM } from '@/features/stats/top-tags';
import { TrendChart } from '@/features/stats/trend-chart';
import { buildTrendChartVM } from '@/features/stats/trend-chart/model/builders';
import { MOTION_VARIANTS } from '@/shared/lib';

interface Props {
  stats: StatsSummary;
}

export const OverviewContent = ({ stats }: Props) => {
  // View Model 빌드 로직을 컴포넌트 내부로 이동 (응집도 향상)
  const difficultyVM = buildDifficultyChartVM(stats);
  const trendVM = buildTrendChartVM(stats);
  const inputTypeVM = buildInputTypeChartVM(stats);
  const topTagsVM = buildTopTagsVM(stats);

  return (
    /* 카드 + 그래프 */
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
  );
}