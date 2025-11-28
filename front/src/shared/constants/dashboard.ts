export type DashboardStat = {
  id: string;
  label: string;
  value: string;
  subLabel?: string;
};

export type ActivityItem = {
  id: number;
  title: string;
  description: string;
  time: string;
};

export type SummaryRow = {
  id: number;
  name: string;
  total: number;
  successRate: number; // 0 ~ 1
};

const STATS: DashboardStat[] = [
  {
    id: 'total-tests',
    label: '총 테스트 케이스',
    value: '1,248',
    subLabel: '지난 7일 +128',
  },
  {
    id: 'completed-runs',
    label: '완료된 테스트 실행',
    value: '86%',
    subLabel: '성공률',
  },
  {
    id: 'open-bugs',
    label: '오픈 이슈',
    value: '23',
    subLabel: 'Critical 5개',
  },
]

const ACTIVITIES: ActivityItem[] = [
  {
    id: 1,
    title: '프론트엔드 E2E 스위트 실행',
    description: 'Playwright · main 브랜치',
    time: '오늘 · 14:32',
  },
  {
    id: 2,
    title: 'API 통합 테스트 실패',
    description: '/payments/checkout 응답 지연',
    time: '오늘 · 10:15',
  },
  {
    id: 3,
    title: '신규 프로젝트 Onboarding 생성',
    description: 'Testea · QA 팀',
    time: '어제 · 18:47',
  },
]

const SUMMARY_ROWS: SummaryRow[] = [
  { id: 1, name: '프론트엔드 회귀 테스트', total: 128, successRate: 0.92 },
  { id: 2, name: '백엔드 API 통합', total: 64, successRate: 0.81 },
  { id: 3, name: '모바일 크로스 브라우징', total: 32, successRate: 0.75 },
]

export const DASHBOARD = {
  STATS,
  ACTIVITIES,
  SUMMARY_ROWS
} as const;
