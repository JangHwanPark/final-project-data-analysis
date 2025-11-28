'use client';

import { SectionHeader } from '@/shared';
import { CHART } from '@/shared/constants';
import { FORMAT, cn } from '@/shared/lib';
import { Cell, Pie, PieChart, ResponsiveContainer } from 'recharts';

import type { DifficultyChartVM } from '../model';

type Props = {
  vm: DifficultyChartVM;
};

export const DifficultyChart = ({ vm }: Props) => {
  const difficultyPieData = vm.items.map((item) => ({
    name: item.label,
    value: item.percentage,
  }));

  return (
    <div
      className={cn(
        'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
        'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none'
      )}
    >
      <SectionHeader title={vm.title} right={vm.rightLabel} />
      <div className="flex h-64 flex-col items-center justify-center gap-4 sm:flex-row">
        {/* 파이 차트 */}
        <div className="h-40 w-40">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={difficultyPieData}
                dataKey="value"
                nameKey="name"
                innerRadius={40}
                outerRadius={60}
                paddingAngle={4}
              >
                {vm.items.map((item, index) => (
                  <Cell key={index} fill={CHART.DIFFICULTY_COLORS[item.key]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* 우측 리스트 */}
        <div className="space-y-1 text-xs">
          {vm.items.map((item) => (
            <div key={item.key} className="flex items-center justify-between gap-3">
              <div className="flex items-center gap-2">
                <span
                  className="h-2 w-2 rounded-full"
                  style={{
                    backgroundColor: CHART.DIFFICULTY_COLORS[item.key],
                  }}
                />
                <span className="font-medium">{item.label}</span>
              </div>
              <span className="text-zinc-500 dark:text-zinc-400">
                {item.count}문제 ({FORMAT.percent(item.percentage / 100, 1)})
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
