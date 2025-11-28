'use client';

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {cn} from '@/shared/lib';
import {SectionHeader} from '@/shared';
import type {TrendChartVM} from '@/features/stats/trend-chart';

type Props = {
  vm: TrendChartVM;
};

export const TrendChart = ({vm}: Props) => {
  return (
    <div
      className={cn(
        'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
        'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
      )}
    >
      <SectionHeader
        title={vm.title}
        right={vm.rightLabel}
      />
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={vm.points}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7"/>
            <XAxis dataKey="date"/>
            <YAxis/>
            <Tooltip/>
            <Bar dataKey="count" fill="#6366f1" radius={[4, 4, 0, 0]}/>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
