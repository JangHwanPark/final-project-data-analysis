import difficulty from '@/shared/data/difficulty.json';
import overview from '@/shared/data/overview.json';
import rawStats from '@/shared/data/raw_stats.json';
import structure from '@/shared/data/structure.json';
import summaryFull from '@/shared/data/summary-full.json';
import summary from '@/shared/data/summary.json';
import tags from '@/shared/data/tags.json';
import type { DataSetItem } from '@/shared/data/types';

// =================================================================
// Type Export
// =================================================================
export type { DataSetItem } from '@/shared/data/types';

// =================================================================
// Data Export
// =================================================================
export const DataSet = {
  Difficulty: difficulty,
  Overview: overview,
  RawStats: rawStats,
  Structure: structure,
  Summary: summary,
  SummaryFull: summaryFull,
  Tags: tags,
} as const;

export const DataSetArray: DataSetItem[] = Object.entries(DataSet).map(([key, value]) => {
  // 키(key)를 제목(Label)으로 변환
  // 예: "rawStats" -> "RAW STATS", "summary-full" -> "SUMMARY FULL"
  const formattedLabel = key
    .replace(/([A-Z])/g, ' $1')
    .replace(/[_-]/g, ' ')
    .toUpperCase();

  return {
    id: key,
    label: formattedLabel,
    data: value,
  };
});

// export const DataSetArray = Object.values(DataSet);

// export const DataSetArray = [
//   { id: 'summary-full', label: 'Summary (Full)', data: summaryFull },
//   { id: 'overview', label: 'Overview Stats', data: overview },
//   { id: 'difficulty', label: 'Difficulty Analysis', data: difficulty },
//   { id: 'tags', label: 'Tag Distribution', data: tags },
//   { id: 'structure', label: 'Structure Analysis', data: structure },
//   { id: 'raw-stats', label: 'Raw Statistics', data: rawStats },
//   { id: 'summary', label: 'Summary (Simple)', data: summary },
// ];