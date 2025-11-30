import { useRouter, usePathname, useSearchParams } from 'next/navigation';
import { DashboardTabKey } from '@/features/dashboard';
import { TABS } from '@/features/dashboard/constants';

export const useDashboardTab = ()  => {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  // URL에서 탭 정보 가져오기 (기본값: overview)
  const rawTab = searchParams.get('tab');
  const activeTab: DashboardTabKey = TABS.IDS.includes(rawTab as DashboardTabKey) ? (rawTab as DashboardTabKey) : 'overview';

  // 탭 변경 핸들러
  const setActiveTab = (tab: DashboardTabKey) => {
    const params = new URLSearchParams(searchParams.toString());
    // params.set('tab', tab);

    // 탭이 'overview'면 쿼리 파라미터를 삭제 -> URL을 깨끗한 '/'로 만듦
    if (tab === 'overview') params.delete('tab');
    // 다른 탭이면 쿼리 파라미터 설정 -> '/?tab=difficulty'
    else params.set('tab', tab);

    // scroll: false로 스크롤 튀는 현상 방지
    // router.push(`${pathname}?${params.toString()}`, { scroll: false });

    // 파라미터가 비어있으면 물음표(?) 없이 경로만 이동
    const query = params.toString();
    const url = query ? `${pathname}?${query}` : pathname;
    router.push(url, { scroll: false });
  };

  return { activeTab, setActiveTab };
}