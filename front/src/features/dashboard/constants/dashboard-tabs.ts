import { DashboardTabKey, TabItem } from '@/features/dashboard';
import { BarChart3, Database, Layers, LayoutDashboard, Tags } from 'lucide-react';








const MENU: TabItem[] = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'difficulty', label: 'Difficulty & Trends', icon: BarChart3 },
  { id: 'tags', label: 'Tags & Categories', icon: Tags },
  { id: 'structure', label: 'Structure', icon: Layers },
  { id: 'raw', label: 'Raw Data', icon: Database },
];

const IDS: DashboardTabKey[] = [
  'overview',
  'difficulty',
  'tags',
  'structure',
  'raw',
];

export const TABS = {
  MENU,
  IDS
}