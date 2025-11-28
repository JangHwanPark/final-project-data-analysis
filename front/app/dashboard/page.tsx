import type { Metadata } from 'next';
import { DASHBOARD } from '@/shared/constants/dashboard';
import { DashboardPage } from '@/view/dashboard';

export const metadata: Metadata = {
  title: '대시보드 | 프로젝트 통계',
  description: '테스트 실행 현황, 이슈, 성공률을 한 눈에 확인하는 대시보드입니다.',
};

export default function DashboardRoute() {
  const stats = DASHBOARD.STATS;
  const activities = DASHBOARD.ACTIVITIES;
  const summaryRows = DASHBOARD.SUMMARY_ROWS;

  return <DashboardPage stats={stats} activities={activities} summaryRows={summaryRows}/>
}
