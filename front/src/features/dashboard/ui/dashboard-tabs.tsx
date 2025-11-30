'use client';

import React from 'react';

import { DashboardTabKey } from '@/features/dashboard';
import { TABS } from '@/features/dashboard/constants';
import { cn } from '@/shared/lib';
import { Select } from '@mantine/core';
import { motion } from 'framer-motion';

interface Props {
  activeTab: DashboardTabKey;
  onChange: (id: DashboardTabKey) => void;
}

export const DashboardTabs = ({ activeTab, onChange }: Props) => {
  return (
    <>
      {/* ----- Mobile Version (md 이하) ----- */}
      <div className="w-full relative md:hidden">
        <Select
          placeholder="메뉴를 선택하세요"
          radius="md"
          size="sm"
          value={activeTab}
          onChange={(value) => value && onChange(value as DashboardTabKey)}
          data={TABS.MENU.map((t) => ({
            value: t.id,
            label: t.label,
          }))}
          classNames={{
            input:
              'w-full h-auto py-3 px-4 rounded-xl bg-zinc-900/80 border border-white/10 text-xl text-white',
            dropdown:
              'p-1 rounded-xl bg-zinc-900 border border-white/10 text-lg text-white shadow-lg bg-zinc-900 border border-white/10 rounded-xl',
            option:
              'p-2 text-zinc-400 hover:text-white hover:bg-zinc-800 data-[checked]:bg-zinc-700 data-[checked]:text-white rounded-lg my-1 transition-colors cursor-pointer',
          }}
        />
      </div>

      {/* ----- Desktop Version ----- */}
      <div className="hidden w-full items-center rounded-2xl border border-white/10 bg-zinc-900/50 p-1.5 backdrop-blur-md md:flex">
        {TABS.MENU.map((tab) => {
          const isActive = activeTab === tab.id;
          const Icon = tab.icon;

          return (
            <button
              key={tab.id}
              onClick={() => onChange(tab.id)}
              className={cn(
                'relative flex flex-1 items-center justify-center gap-2 rounded-xl py-2.5 text-sm font-medium transition-colors hover:cursor-pointer md:text-base',
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
    </>
  );
};
