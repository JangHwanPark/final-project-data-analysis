'use client';

import {ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, CartesianGrid, Cell} from 'recharts';

type SharedBarChartProps = {
  data: Array<{ name: string; value: number }>;
  xKey: string;
  valueKey: string;
  colors?: string[];
  showLegend?: boolean;
  className?: string;
};

export const SharedBarChart = ({
  data,
  xKey,
  valueKey,
  colors = ['#6366f1'],
  showLegend = false,
}: SharedBarChartProps) => {
  return (
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7"/>
          <XAxis dataKey={xKey}/>
          <YAxis/>
          <Tooltip/>
          {showLegend && <Legend />}
          <Bar dataKey={valueKey}>
            {data.map((_, i) => (
                <Cell key={i} fill={colors[i % colors.length]}/>
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
  );
}
