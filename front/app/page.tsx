import { Suspense } from 'react';

import type { Metadata } from 'next';

import { summary } from '@/entities/summary';
import type { RawStatsSummary } from '@/entities/summary/types';
import rawSummary from '@/shared/data/summary.json';
import { MainPage } from '@/view/main';

export const metadata: Metadata = {
  title: '대시보드 | 프로젝트 통계',
  description: '테스트 실행 현황, 이슈, 성공률을 한 눈에 확인하는 대시보드입니다.',
};

export default function HomeRoute() {
  const stats = summary.mapper.toStats(rawSummary as RawStatsSummary);
  return (
    <Suspense
      fallback={<div className="p-8 text-center text-zinc-500">대시보드를 불러오는 중...</div>}
    >
      <MainPage stats={stats} />
    </Suspense>
  );
}
