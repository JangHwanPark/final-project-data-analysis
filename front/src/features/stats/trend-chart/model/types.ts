export type TrendChartPoint = {
  date: string;
  count: number;
};

export type TrendChartVM = {
  title: string;
  rightLabel: string;
  points: TrendChartPoint[];
};