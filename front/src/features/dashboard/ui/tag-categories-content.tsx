'use client';

import React from 'react';
import { motion } from 'framer-motion';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  Cell, PieChart, Pie
} from 'recharts';
import { MOTION } from '@/shared/lib/motion';

// 백엔드 데이터 타입 (tags.json 구조)
interface TagsStats {
  metrics: {
    top_tags_distribution: Record<string, number>;
    algorithm_category_distribution: {
      counts: Record<string, number>;
      percentages: Record<string, number>;
    };
    input_type_distribution: {
      counts: Record<string, number>;
    };
  };
}

interface Props {
  data: TagsStats;
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

export const TagsContent = ({ data }: Props) => {
  const { metrics } = data;

  // 1. Top Tags 데이터 변환 (Object -> Array)
  const topTagsData = Object.entries(metrics?.top_tags_distribution || {})
    .map(([tag, count]) => ({ name: tag, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 10); // 상위 10개만

  // 2. Algorithm Category 데이터 변환
  const algoData = Object.entries(metrics?.algorithm_category_distribution?.counts || {})
    .map(([category, count]) => ({ name: category, value: count }))
    .sort((a, b) => b.value - a.value);

  // 3. Input Type 데이터 변환
  const inputTypeData = Object.entries(metrics?.input_type_distribution?.counts || {})
    .map(([type, count]) => ({ name: type, value: count }));

  if (!metrics) {
      return <div className="text-center text-zinc-500 py-10">데이터를 불러오는 중입니다...</div>;
  }

  return (
    <motion.section
      variants={MOTION.STAGGER_CONTAINER(0.06)}
      initial="hidden"
      animate="show"
      className="grid grid-cols-1 gap-6 md:grid-cols-2"
    >
      {/* 가장 많이 출제된 태그 (가로 막대) */}
      <motion.div
        variants={MOTION.FADEINUP(0.02)}
        className="col-span-1 rounded-3xl border border-white/10 bg-zinc-900/30 p-6 md:col-span-2"
      >
        <h3 className="mb-2 text-lg font-bold text-white">🔥 Top 10 Frequent Tags</h3>
        <p className="mb-6 text-sm text-zinc-400">가장 자주 등장하는 문제 유형 상위 10개입니다.</p>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={topTagsData} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" horizontal={false} />
              <XAxis type="number" stroke="#666" />
              <YAxis dataKey="name" type="category" stroke="#999" width={100} tick={{fontSize: 12}} />
              <Tooltip
                contentStyle={{ backgroundColor: '#18181b', border: '1px solid #333', color: '#fff' }}
                cursor={{ fill: 'rgba(255,255,255,0.05)' }}
              />
              <Bar dataKey="count" fill="#8884d8" radius={[0, 4, 4, 0]} barSize={20}>
                {topTagsData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* 알고리즘 카테고리 분포 (파이 차트) */}
      <motion.div
        variants={MOTION.FADEINUP(0.04)}
        className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
      >
        <h3 className="mb-4 text-lg font-bold text-white">🗂️ Algorithm Categories</h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={algoData}
                cx="50%"
                cy="50%"
                innerRadius={60}
                outerRadius={80}
                paddingAngle={5}
                dataKey="value"
              >
                {algoData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip contentStyle={{ backgroundColor: '#18181b', border: '1px solid #333', color: '#fff' }} />
              <Legend verticalAlign="bottom" height={36} iconType="circle" />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* 입력 데이터 타입 분포 (심플 리스트 or 바 차트) */}
      <motion.div
        variants={MOTION.FADEINUP(0.06)}
        className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
      >
        <h3 className="mb-4 text-lg font-bold text-white">📥 Input Data Types</h3>
        <div className="flex h-[300px] flex-col justify-center gap-4 overflow-y-auto pr-2">
            {inputTypeData.map((item, idx) => (
                <div key={item.name} className="flex items-center gap-4">
                    <div className="w-24 text-sm font-medium text-zinc-400 truncate">{item.name}</div>
                    <div className="flex-1 overflow-hidden rounded-full bg-zinc-800 h-2">
                        <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${(item.value / inputTypeData.reduce((acc, cur) => acc + cur.value, 0)) * 100}%` }}
                            transition={{ duration: 1, delay: idx * 0.1 }}
                            className="h-full rounded-full"
                            style={{ backgroundColor: COLORS[idx % COLORS.length] }}
                        />
                    </div>
                    <div className="w-12 text-right text-sm font-bold text-white">{item.value}</div>
                </div>
            ))}
        </div>
      </motion.div>
    </motion.section>
  );
}