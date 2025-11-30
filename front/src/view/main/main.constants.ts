import { DashboardTabKey, HeaderConfig } from '@/features/dashboard';







const COMMON = {
  BADGE_TEXT: '알고리즘 문제 세트 통계',
  META_LABEL: '마지막 동기화:',
} as const;

const OVERVIEW = {
  TITLE: '메인 대시보드',
  DESCRIPTION: 'Coding Questions Dataset의 데이터를 기반으로 구성된 난이도, 태그, 입력 타입 분포 통계입니다.',
} as const satisfies HeaderConfig;

const DIFFICULTY = {
  TITLE: 'Difficulty Insights',
  DESCRIPTION: '난이도 분포와 난이도별 추이를 분석합니다.',
};

const TAGS = {
  TITLE: 'Tag & Topics',
  DESCRIPTION: '문제에 사용된 태그/주제를 기준으로 분포를 확인합니다.',
} as const satisfies HeaderConfig;

const STRUCTURE = {
  TITLE: 'Problem Structure',
  DESCRIPTION: '입력/출력/예시/제약 등 문제 구조를 분석합니다.',
} as const satisfies HeaderConfig;

const RAW = {
  TITLE: 'Raw Dataset',
  DESCRIPTION: '원본 데이터를 그대로 테이블로 확인합니다.',
} as const satisfies HeaderConfig;

const HEADERS = {
  overview: OVERVIEW,
  difficulty: DIFFICULTY,
  tags: TAGS,
  structure: STRUCTURE,
  raw: RAW,
} satisfies Record<DashboardTabKey, HeaderConfig>;

export const MAIN_DASHBOARD = {
  COMMON,
  HEADERS,
} as const;
