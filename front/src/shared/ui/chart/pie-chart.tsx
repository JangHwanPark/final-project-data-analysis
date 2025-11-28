'use client';

import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';

type SharedPieChartProps = {
  data: Array<{ name: string; value: number }>;
  colors: string[] | Record<string, string>;
  innerRadius?: number;
  outerRadius?: number;
};

export const SharedPieChart = ({
  data,
  colors,
  innerRadius = 40,
  outerRadius = 60,
}: SharedPieChartProps)=> {
  const getColor = (item: any, index: number) => {
    if (Array.isArray(colors)) return colors[index % colors.length];
    return colors[item.name] || '#8884d8';
  };

  return (
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Tooltip />
          <Pie
              data={data}
              dataKey="value"
              nameKey="name"
              innerRadius={innerRadius}
              outerRadius={outerRadius}
              paddingAngle={4}
          >
            {data.map((item, i) => (
                <Cell key={i} fill={getColor(item, i)} />
            ))}
          </Pie>
        </PieChart>
      </ResponsiveContainer>
  );
}
