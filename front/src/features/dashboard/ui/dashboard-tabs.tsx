'use client';

import React from 'react';

import { cn } from '@/shared/lib';
import { motion } from 'framer-motion';
import { BarChart3, Database, Layers, LayoutDashboard, Tags } from 'lucide-react';

// 탭 ID 타입 정의 (백엔드 데이터 구조와 매핑될 예정)
export type TabId = 'overview' | 'difficulty' | 'tags' | 'structure' | 'raw';

interface TabItem {
  id: TabId;
  label: string;
  icon: React.ElementType;
}

// 탭 목록 정의
const TABS: TabItem[] = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'difficulty', label: 'Difficulty & Trends', icon: BarChart3 },
  { id: 'tags', label: 'Tags & Categories', icon: Tags },
  { id: 'structure', label: 'Structure', icon: Layers },
  { id: 'raw', label: 'Raw Data', icon: Database },
];

interface DashboardTabsProps {
  activeTab: TabId;
  onChange: (id: TabId) => void;
}

export const DashboardTabs = ({ activeTab, onChange }: DashboardTabsProps) => {
  return (
    <div className="flex w-full items-center rounded-2xl border border-white/10 bg-zinc-900/50 p-1.5 backdrop-blur-md">
      {TABS.map((tab) => {
        const isActive = activeTab === tab.id;
        const Icon = tab.icon;

        return (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={cn(
              'relative flex flex-1 items-center justify-center gap-2 rounded-xl py-2.5 text-sm font-medium transition-colors md:text-base',
              isActive ? 'text-white' : 'text-zinc-400 hover:text-zinc-200'
            )}
          >
            {/* 활성화된 탭 배경 애니메이션 (layoutId로 부드러운 이동) */}
            {isActive && (
              <motion.div
                layoutId="active-tab-bg"
                className="absolute inset-0 rounded-xl bg-white/10 shadow-sm"
                transition={{ type: 'spring', bounce: 0.2, duration: 0.6 }}
              />
            )}

            <span className="relative z-10 flex items-center gap-2">
              <Icon className="h-4 w-4" />
              <span className="hidden sm:inline">{tab.label}</span>
            </span>
          </button>
        );
      })}
    </div>
  );
};
