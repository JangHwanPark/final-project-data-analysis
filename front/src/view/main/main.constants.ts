export const MAIN_DASHBOARD = {
  BADGE_TEXT: '알고리즘 문제 세트 통계',
  TITLE: '메인 대시보드',
  DESCRIPTION: (days: number) =>
    `최근 ${days}일 동안 수집한 문제들의 난이도, 태그, 입력 타입 분포를 한 눈에 정리한 메인 페이지입니다.`,
  META_LABEL: '최신 데이터 기준:',
} as const;
