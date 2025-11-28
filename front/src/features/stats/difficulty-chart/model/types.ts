import type { DifficultyKey } from '@/entities/summary/types';

export type DifficultyChartItem = {
  key: DifficultyKey;
  label: string;      // Easy / Medium / Hard
  count: number;      // 개수
  percentage: number; // 0~100 (%)
};

export type DifficultyChartVM = {
  title: string;      // 난이도 분포
  rightLabel: string; // Hard / Medium / Easy 비율
  items: DifficultyChartItem[];
};