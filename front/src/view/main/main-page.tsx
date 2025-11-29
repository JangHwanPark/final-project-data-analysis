'use client';
import React from 'react';

import type { StatsSummary } from '@/entities/summary/types';
import {
  DashboardTabs,
  DifficultyContent,
  OverviewContent,
  RawDataContent,
  StructureContent,
  TagsContent,
  useDashboardTab,
} from '@/features/dashboard';
import { MAIN_DASHBOARD } from '@/view/main/main.constants';
import { MainHeader } from '@/widgets';
import { format } from 'date-fns';
import { AnimatePresence, motion } from 'framer-motion';

type Props = {
  stats: StatsSummary;
};

export function MainPage({ stats }: Props) {
  const { overview } = stats;
  const latest = format(new Date(overview.latestCreatedAt), 'yyyy-MM-dd');
  const { activeTab, setActiveTab } = useDashboardTab();

  return (
    <main className="mx-auto flex max-w-6xl flex-1 flex-col justify-center gap-8 px-4 py-8 md:px-8 md:py-10">
      {/* 헤더 */}
      <MainHeader
        badgeText={MAIN_DASHBOARD.BADGE_TEXT}
        title={MAIN_DASHBOARD.TITLE}
        description={MAIN_DASHBOARD.DESCRIPTION}
        metaLabel={MAIN_DASHBOARD.META_LABEL}
        metaValue={latest}
      />
      {/* 탭 콘텐츠 영역 */}
      <DashboardTabs activeTab={activeTab} onChange={setActiveTab} />

      {/* 탭 콘텐츠 영역 (조건부 렌더링) */}
      <AnimatePresence mode="wait">
        {activeTab === '/' && (
          <motion.div
            key="overview"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <OverviewContent stats={stats} />
          </motion.div>
        )}

        {/* Difficulty 탭은 metrics 데이터를 필요로 하는 구조로 가정 */}
        {activeTab === 'difficulty' && (
          <motion.div
            key="difficulty"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <DifficultyContent data={{ metrics: stats.metrics }} />
          </motion.div>
        )}

        {activeTab === 'tags' && (
          <motion.div
            key="tags"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <TagsContent data={{ metrics: stats.metrics }} />
          </motion.div>
        )}

        {activeTab === 'structure' && (
          <motion.div
            key="structure"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <StructureContent data={{ metrics: stats.metrics }} />
          </motion.div>
        )}

        {activeTab === 'raw' && (
          <motion.div
            key="raw"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <RawDataContent data={stats} />
          </motion.div>
        )}
      </AnimatePresence>
      {/* Overview Content - Route: (/) */}
      <OverviewContent stats={stats} />
    </main>
  );
}
