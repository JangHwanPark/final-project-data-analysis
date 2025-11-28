import {DifficultyKey} from "@/entities/summary/types";

const DIFFICULTY_COLORS: Record<DifficultyKey, string> = {
  Easy: '#22c55e',
  Medium: '#eab308',
  Hard: '#ef4444',
};

const INPUT_TYPE_COLORS = [
  '#3b82f6',
  '#22c55e',
  '#a855f7',
  '#f97316',
  '#06b6d4',
  '#e11d48',
];

export const CHART = {
  DIFFICULTY_COLORS,
  INPUT_TYPE_COLORS
} as const;