'use client';
import React from 'react';
import {cn} from "@/shared/lib";
import {InputTypeChartVM} from "@/features/stats/input-type-chart/model";
import {SectionHeader, SharedBarChart} from "@/shared";
import { CHART } from '@/shared/constants';

type Props = {
  vm: InputTypeChartVM;
};

export const InputTypeChart = ({vm}: Props) => {
  return (
    <div
      className={cn(
        'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
        'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
      )}
    >
      <SectionHeader title="입력 타입 분포" right="Array / String / Tree 등" />
      <div className="h-64">
        <SharedBarChart
          data={vm.items}
          xKey="name"
          valueKey="value"
          colors={CHART.INPUT_TYPE_COLORS}
          showLegend={true}
        />
      </div>
    </div>
  );
};