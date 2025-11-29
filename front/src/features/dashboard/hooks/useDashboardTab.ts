import { useRouter, usePathname, useSearchParams } from 'next/navigation';
import { TabId } from '@/features/dashboard/ui/DashboardTabs';

export const useDashboardTab = ()  => {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  // URL에서 탭 정보 가져오기 (기본값: overview)
  const activeTab = (searchParams.get('tab') as TabId) || 'overview';

  // 탭 변경 핸들러
  const setActiveTab = (tab: TabId) => {
    const params = new URLSearchParams(searchParams.toString());
    params.set('tab', tab);

    // scroll: false로 스크롤 튀는 현상 방지
    router.push(`${pathname}?${params.toString()}`, { scroll: false });
  };

  return { activeTab, setActiveTab };
}