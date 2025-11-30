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
import { difficulty } from '@/entities/difficulty';
import { tags } from '@/entities/tags';
import { structure } from '@/entities/structure';

type Props = {
  stats: StatsSummary;
};

export function MainPage({ stats }: Props) {
  const { overview } = stats;
  const latest = format(new Date(overview.latestCreatedAt), 'yyyy-MM-dd');
  const { activeTab, setActiveTab } = useDashboardTab();

  // ====================================================
  // 탭별 데이터를 매핑
  // MainPage는 Full Summary (StatsSummary)를 받으므로 Content에 전달할 때
  // 해당 Content가 요구하는 DTO 구조로 변환 || 엔티티 매퍼를 거쳐야함
  // ====================================================
  // Difficulty Data 매핑
  const difficultyData = difficulty.mapper.toDifficultyStats({
    // StatsSummary에는 timestamp가 없으므로 임시 값 사용(SummaryInfo 정의 필요)
    // Raw Metrics 전체를 넘겨줌(DifficultyContent가 필요한 metrics를 매퍼가 찾아냄)
    summary_info: { generated_at: 'N/A' },
    metrics: stats.metrics,
  });

  // Tags Data 매핑
  const tagsData = tags.mapper.toTagsStats({
    summary_info: { generated_at: 'N/A' },
    metrics: stats.metrics,
  });

  // Structure Data 매핑
  const structureData = structure.mapper.toStructureStats({
    summary_info: { generated_at: 'N/A' },
    metrics: stats.metrics,
  });

  // 헤더 매핑
  const HEADER_CONFIG = MAIN_DASHBOARD.HEADERS[activeTab];

  return (
    <main className="mx-auto flex w-6xl max-w-6xl flex-1 flex-col justify-center gap-8 px-4 py-8 md:px-8 md:py-10">
      {/* 헤더 */}
      <MainHeader
        badgeText={MAIN_DASHBOARD.COMMON.BADGE_TEXT}
        metaLabel={MAIN_DASHBOARD.COMMON.META_LABEL}
        title={HEADER_CONFIG.TITLE}
        description={HEADER_CONFIG.DESCRIPTION}
        metaValue={latest}
      />
      {/* 탭 콘텐츠 영역 */}
      <DashboardTabs activeTab={activeTab} onChange={setActiveTab} />

      {/* 탭 콘텐츠 영역 (조건부 렌더링) */}
      <AnimatePresence mode="wait">
        {activeTab === 'overview' && (
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
            <DifficultyContent data={difficultyData} />
          </motion.div>
        )}

        {activeTab === 'tags' && (
          <motion.div
            key="tags"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <TagsContent data={tagsData} />
          </motion.div>
        )}

        {activeTab === 'structure' && (
          <motion.div
            key="structure"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <StructureContent data={structureData} />
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
    </main>
  );
}
