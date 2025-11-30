'use client';

import React from 'react';

import { cn } from '@/shared/lib';
import { motion } from 'framer-motion';
import { DashboardTabKey } from '@/features/dashboard';
import { TABS } from '@/features/dashboard/constants';

interface Props {
  activeTab: DashboardTabKey;
  onChange: (id: DashboardTabKey) => void;
}

export const DashboardTabs = ({ activeTab, onChange }: Props) => {
  return (
    <div className="flex w-full items-center rounded-2xl border border-white/10 bg-zinc-900/50 p-1.5 backdrop-blur-md">
      {TABS.MENU.map((tab) => {
        const isActive = activeTab === tab.id;
        const Icon = tab.icon;

        return (
          <button
            key={tab.id}
            onClick={() => onChange(tab.id)}
            className={cn(
              'relative flex flex-1 items-center justify-center gap-2 rounded-xl py-2.5 text-sm font-medium transition-colors md:text-base hover:cursor-pointer',
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
