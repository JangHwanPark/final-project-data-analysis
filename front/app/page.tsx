import type { Metadata } from 'next';
import rawSummary from '@/shared/data/summary.json';
import { MainPage } from '@/view/main';
import type {RawStatsSummary} from "@/entities/summary/types";
import { summary } from '@/entities/summary';

export const metadata: Metadata = {
  title: '대시보드 | 프로젝트 통계',
  description: '테스트 실행 현황, 이슈, 성공률을 한 눈에 확인하는 대시보드입니다.',
};

export default function HomeRoute() {
  const stats = summary.mapper.toStats(rawSummary as RawStatsSummary);
  return <MainPage stats={stats}/>
};