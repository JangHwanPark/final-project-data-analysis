'use client';

import React from 'react';

import { motion } from 'framer-motion';
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

import { MOTION } from '@/shared/lib/motion';


// 백엔드 데이터 타입 (structure.json 구조)
interface StructureStats {
  metrics: {
    description_length_bucket_distribution: Record<string, number>;
    constraints_count_distribution: Record<string, number>;
    example_count_distribution: Record<string, number>;
    test_case_count_distribution: Record<string, number>;
  };
}

interface Props {
  data: StructureStats;
}

export const StructureContent = ({ data }: Props) => {
  const { metrics } = data;

  // 데이터가 없을 경우를 대비한 안전 장치
  if (!metrics) {
    return <div className="p-10 text-center text-zinc-500">데이터를 불러오는 중입니다...</div>;
  }

  // 1. 설명 길이 분포 (히스토그램용 데이터)
  const lengthData = Object.entries(metrics.description_length_bucket_distribution || {}).map(
    ([range, count]) => ({ range, count })
  );

  // 2. 제약조건 수 분포
  const constraintData = Object.entries(metrics.constraints_count_distribution || {}).map(
    ([countKey, value]) => ({ countKey, value })
  );

  // 3. 예제 개수 분포
  const exampleData = Object.entries(metrics.example_count_distribution || {}).map(([k, v]) => ({
    k,
    v,
  }));

  return (
    <motion.section
      variants={MOTION.STAGGER_CONTAINER(0.06)}
      initial="hidden"
      animate="show"
      className="flex flex-col gap-6"
    >
      {/* 문제 설명 길이 분포 (Area Chart로 분포 느낌 강조) */}
      <motion.div
        variants={MOTION.FADEINUP(0.02)}
        className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
      >
        <div className="mb-6">
          <h3 className="text-lg font-bold text-white">📝 Description Length Distribution</h3>
          <p className="text-xs text-zinc-500">문제 설명의 글자 수 구간별 분포입니다.</p>
        </div>
        <div className="h-[250px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={lengthData}>
              <defs>
                <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                  <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
              <XAxis dataKey="range" stroke="#666" fontSize={12} />
              <YAxis stroke="#666" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#18181b',
                  border: '1px solid #333',
                  color: '#fff',
                }}
              />
              <Area
                type="monotone"
                dataKey="count"
                stroke="#8884d8"
                fillOpacity={1}
                fill="url(#colorCount)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
        {/* 제약조건 개수 (Bar Chart) */}
        <motion.div
          variants={MOTION.FADEINUP(0.04)}
          className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
        >
          <h3 className="mb-4 text-lg font-bold text-white">⚠️ Constraints Count</h3>
          <p className="mb-4 text-xs text-zinc-500">문제당 포함된 제약조건의 개수입니다.</p>
          <div className="h-[250px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={constraintData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                <XAxis dataKey="countKey" stroke="#666" fontSize={12} />
                <Tooltip
                  cursor={{ fill: 'transparent' }}
                  contentStyle={{
                    backgroundColor: '#18181b',
                    border: '1px solid #333',
                    color: '#fff',
                  }}
                />
                <Bar dataKey="value" fill="#82ca9d" radius={[4, 4, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>

        {/* 예제 개수 (Bar Chart) */}
        <motion.div
          variants={MOTION.FADEINUP(0.06)}
          className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
        >
          <h3 className="mb-4 text-lg font-bold text-white">💡 Example Cases Count</h3>
          <p className="mb-4 text-xs text-zinc-500">문제 지문에 제공된 예제 케이스의 개수입니다.</p>
          <div className="h-[250px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={exampleData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
                <XAxis dataKey="k" stroke="#666" fontSize={12} />
                <Tooltip
                  cursor={{ fill: 'transparent' }}
                  contentStyle={{
                    backgroundColor: '#18181b',
                    border: '1px solid #333',
                    color: '#fff',
                  }}
                />
                <Bar dataKey="v" fill="#ffc658" radius={[4, 4, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      </div>
    </motion.section>
  );
}
