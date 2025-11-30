'use client';

import React from 'react';

import { DifficultyKey } from '@/entities/dashboard';
import type { DifficultyStats } from '@/entities/difficulty';
import { MOTION_VARIANTS } from '@/shared/lib';
import { motion } from 'framer-motion';
import {
  Bar,
  BarChart,
  CartesianGrid,
  ComposedChart,
  Legend,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

interface Props {
  data: DifficultyStats;
}

export const DifficultyContent = ({ data }: Props) => {
  const { metrics, complexityData, difficultyDistribution, difficultyOverTime } = data;

  // 데이터가 없을 경우를 대비한 안전 장치 (컴포넌트가 최소한의 방어)
  if (!metrics || !complexityData || !difficultyDistribution || !difficultyOverTime) {
    return (
      <div className="flex h-[400px] w-full items-center justify-center rounded-3xl border border-white/10 bg-zinc-900/30 text-zinc-500">
        데이터를 불러오는 중이거나 없습니다. (매퍼에서 데이터가 생성되지 않았을 수 있습니다.)
      </div>
    );
  }

  // DUMP: 차트 렌더링에 필요한 추가 데이터 안전 추출
  const diffCounts = difficultyDistribution.counts;
  const diffPercents = difficultyDistribution.percentages;
  const trendData = difficultyOverTime;
  const chartComplexityData = complexityData;
  const difficultyLevels: DifficultyKey[] = ['Easy', 'Medium', 'Hard'];

  return (
    <motion.section
      variants={MOTION_VARIANTS.STAGGER_CONTAINER(0.06)}
      initial="hidden"
      animate="show"
      className="flex flex-col gap-6"
    >
      {/* 상단: 난이도별 요약 카드 */}
      <motion.div
        variants={MOTION_VARIANTS.FADEINUP(0.02)}
        className="grid grid-cols-1 gap-4 md:grid-cols-3"
      >
        {difficultyLevels.map((level) => (
          <div
            key={level}
            className="relative overflow-hidden rounded-2xl border border-white/10 bg-zinc-900/50 p-6 backdrop-blur-sm"
          >
            <div
              className={`absolute top-4 right-4 h-2 w-2 rounded-full ${
                level === 'Easy'
                  ? 'bg-green-500'
                  : level === 'Medium'
                    ? 'bg-yellow-500'
                    : 'bg-red-500'
              }`}
            />
            <h3 className="text-sm font-medium text-zinc-400">{level} Questions</h3>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-3xl font-bold text-white">
                {diffCounts[level as DifficultyKey] || 0}
              </span>
              <span className="text-sm text-zinc-500">
                ({diffPercents[level as DifficultyKey] || 0}%)
              </span>
            </div>
          </div>
        ))}
      </motion.div>

      {/* 중단: 시계열 트렌드 (Stacked Bar) */}
      <motion.div
        variants={MOTION_VARIANTS.FADEINUP(0.04)}
        className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
      >
        <h3 className="mb-6 text-lg font-bold text-white">Daily Difficulty Volume</h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={trendData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
              <XAxis dataKey="date" stroke="#666" fontSize={12} tickMargin={10} />
              <YAxis stroke="#666" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#18181b',
                  border: '1px solid #333',
                  borderRadius: '8px',
                }}
                cursor={{ fill: 'rgba(255,255,255,0.05)' }}
              />
              <Legend />
              {/* Stacked Bars */}
              <Bar dataKey="Easy" stackId="a" fill="#22c55e" radius={[0, 0, 0, 0]} />
              <Bar dataKey="Medium" stackId="a" fill="#eab308" radius={[0, 0, 0, 0]} />
              <Bar dataKey="Hard" stackId="a" fill="#ef4444" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </motion.div>

      {/* 하단: 복잡도 분석 (Composed Chart: Bar + Line) */}
      <motion.div
        variants={MOTION_VARIANTS.FADEINUP(0.06)}
        className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
      >
        <h3 className="mb-6 text-lg font-bold text-white">Complexity Metrics by Difficulty</h3>
        <div className="h-[300px] w-full">
          <ResponsiveContainer width="100%" height="100%">
            <ComposedChart data={chartComplexityData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" vertical={false} />
              <XAxis dataKey="name" stroke="#666" fontSize={12} />

              {/* 왼쪽 Y축: 설명 길이 */}
              <YAxis
                yAxisId="left"
                stroke="#8884d8"
                label={{
                  value: 'Avg Desc Length (chars)',
                  angle: -90,
                  position: 'insideLeft',
                  fill: '#8884d8',
                }}
              />

              {/* 오른쪽 Y축: 테스트 케이스 수 */}
              <YAxis
                yAxisId="right"
                orientation="right"
                stroke="#ff7300"
                label={{
                  value: 'Avg Test Cases',
                  angle: 90,
                  position: 'insideRight',
                  fill: '#ff7300',
                }}
              />

              <Tooltip contentStyle={{ backgroundColor: '#18181b', border: '1px solid #333' }} />
              <Legend />

              <Bar
                yAxisId="left"
                dataKey="descLength"
                name="Avg Description Length"
                fill="#8884d8"
                barSize={60}
                radius={[4, 4, 0, 0]}
              />
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="testCases"
                name="Avg Test Cases"
                stroke="#ff7300"
                strokeWidth={3}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </div>
        <p className="mt-4 text-center text-xs text-zinc-500">
          * 막대 그래프는 평균 문제 길이(글자 수), 꺾은선 그래프는 평균 테스트 케이스 수를
          나타냅니다.
        </p>
      </motion.div>
    </motion.section>
  );
};
