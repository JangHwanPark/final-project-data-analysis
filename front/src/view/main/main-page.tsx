'use client';

import {format} from 'date-fns';
import {motion} from 'framer-motion';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  Cell,
} from 'recharts';
import type {StatsSummary, DifficultyKey} from '@/entities/summary/types';
import {cn, MOTION_VARIANTS, FORMAT} from '@/shared/lib';
import {Footer} from "@/widgets/footer";
import {GlobalNavbar} from "@/widgets/global-navbar/global-navbar";
import {SectionHeader, SharedBarChart} from "@/shared";

type MainPageProps = {
  stats: StatsSummary;
};

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

export function MainPage({stats}: MainPageProps) {
  const {
    overview,
    difficultyDistribution,
    problemsPerDay,
    difficultyOverTime,
    inputTypeDistribution,
    topTagsDistribution,
    duplicateTitleCount,
  } = stats;

  const earliest = format(new Date(overview.earliestCreatedAt), 'yyyy-MM-dd');
  const latest = format(new Date(overview.latestCreatedAt), 'yyyy-MM-dd');

  const difficultyPieData = (Object.keys(
      difficultyDistribution.percentages,
  ) as DifficultyKey[]).map((key) => ({
    name: key,
    value: difficultyDistribution.percentages[key],
  }));

  const inputTypeBarData = Object.entries(
      inputTypeDistribution.percentages,
  ).map(([name, value]) => ({
    name,
    value,
  }));

  const summaryCards = [
    {
      id: 'total',
      label: '총 문제 수',
      value: overview.totalQuestions.toLocaleString('ko-KR'),
      subLabel: `${earliest} ~ ${latest} (${overview.daysSpan}일)`,
    },
    {
      id: 'difficulty',
      label: '난이도 분포',
      value: `${difficultyDistribution.counts.Hard}H / ${difficultyDistribution.counts.Medium}M / ${difficultyDistribution.counts.Easy}E`,
      subLabel: 'Hard / Medium / Easy',
    },
    {
      id: 'duplicates',
      label: '중복 제목 수',
      value: duplicateTitleCount.toString(),
      subLabel: '비슷한 유형의 문제들',
    },
  ];

  const topTags = Object.entries(topTagsDistribution)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);

  return (
      <>
        <GlobalNavbar/>
        <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-8 px-4 py-8 md:px-8 md:py-10">
          {/* 헤더 */}
          <header className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
            <div className="space-y-2">
              <p className="inline-flex items-center gap-2 rounded-full bg-zinc-100 px-3 py-1 text-xs font-medium text-zinc-600 dark:bg-zinc-900 dark:text-zinc-300">
                <span className="inline-flex h-1.5 w-1.5 rounded-full bg-emerald-500"/>
                알고리즘 문제 세트 통계
              </p>
              <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
                메인 대시보드
              </h1>
              <p className="max-w-xl text-sm text-zinc-600 dark:text-zinc-400">
                최근 {overview.daysSpan}일 동안 수집한 문제들의 난이도, 태그, 입력 타입
                분포를 한 눈에 정리한 메인 페이지입니다.
              </p>
            </div>
            <div className="text-xs text-zinc-500 dark:text-zinc-400">
              최신 데이터 기준:{' '}
              <span className="font-medium text-zinc-700 dark:text-zinc-200">
            {latest}
          </span>
            </div>
          </header>

          {/* 카드 + 그래프 */}
          <motion.section
              variants={MOTION_VARIANTS.STAGGER_CONTAINER(0.06)}
              initial="hidden"
              animate="show"
              className="flex flex-col gap-6"
          >
            {/* 상단 카드 */}
            <motion.div
                variants={MOTION_VARIANTS.FADEINUP(0.02)}
                className="grid gap-4 sm:grid-cols-3"
            >
              {summaryCards.map((card) => (
                  <div
                      key={card.id}
                      className={cn(
                          'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
                          'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
                      )}
                  >
                    <p className="text-xs font-medium text-zinc-500 dark:text-zinc-400">
                      {card.label}
                    </p>
                    <p className="mt-2 text-2xl font-semibold tracking-tight">
                      {card.value}
                    </p>
                    {card.subLabel && (
                        <p className="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
                          {card.subLabel}
                        </p>
                    )}
                  </div>
              ))}
            </motion.div>

            {/* 중간: 날짜별 수 + 난이도 파이 */}
            <motion.div
                variants={MOTION_VARIANTS.FADEINUP(0.04)}
                className="grid gap-6 md:grid-cols-[1.5fr_1fr]"
            >
              {/* 날짜별 문제 수 */}
              <div
                  className={cn(
                      'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
                      'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
                  )}
              >
                <SectionHeader title="날짜별 문제 수" right={`총 ${overview.totalQuestions.toLocaleString("ko-KR")}문제`}/>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={problemsPerDay}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7"/>
                      <XAxis dataKey="date"/>
                      <YAxis/>
                      <Tooltip/>
                      <Bar
                          dataKey="count"
                          fill="#6366f1"
                          radius={[4, 4, 0, 0]}
                      />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* 난이도 파이 차트 */}
              <div
                  className={cn(
                      'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
                      'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
                  )}
              >
                <SectionHeader title="난이도 분포" right="Hard / Medium / Easy 비율"/>
                <div className="flex h-64 flex-col items-center justify-center gap-4 sm:flex-row">
                  <div className="h-40 w-40">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                            data={difficultyPieData}
                            dataKey="value"
                            nameKey="name"
                            innerRadius={40}
                            outerRadius={60}
                            paddingAngle={4}
                        >
                          {difficultyPieData.map((entry, index) => {
                            const key = entry.name as DifficultyKey;
                            return (
                                <Cell
                                    key={`cell-${index}`}
                                    fill={DIFFICULTY_COLORS[key]}
                                />
                            );
                          })}
                        </Pie>
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                  <div className="space-y-1 text-xs">
                    {(Object.keys(
                        difficultyDistribution.counts,
                    ) as DifficultyKey[])
                        .sort(
                            (a, b) =>
                                difficultyDistribution.counts[b] -
                                difficultyDistribution.counts[a],
                        )
                        .map((key) => (
                            <div
                                key={key}
                                className="flex items-center justify-between gap-3"
                            >
                              <div className="flex items-center gap-2">
                        <span
                            className="h-2 w-2 rounded-full"
                            style={{backgroundColor: DIFFICULTY_COLORS[key]}}
                        />
                                <span className="font-medium">{key}</span>
                              </div>
                              <span className="text-zinc-500 dark:text-zinc-400">
                        {difficultyDistribution.counts[key]}문제 (
                                {FORMAT.percent(
                                    difficultyDistribution.percentages[key] / 100,
                                    1,
                                )}
                                )
                      </span>
                            </div>
                        ))}
                  </div>
                </div>
              </div>
            </motion.div>

            {/* 하단: 입력 타입 분포 + 상위 태그 */}
            <motion.div
                variants={MOTION_VARIANTS.FADEINUP(0.06)}
                className="grid gap-6 md:grid-cols-[1.5fr_1fr]"
            >
              {/* 입력 타입 분포 */}
              <div
                  className={cn(
                      'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
                      'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
                  )}
              >
                <div
                    className="mb-3 flex items-center justify-between text-sm font-medium text-zinc-700 dark:text-zinc-200">
                  <span>입력 타입 분포</span>
                  <span className="text-xs text-zinc-500 dark:text-zinc-400">
                Array / String / Tree 등
              </span>
                </div>
                <div className="h-64">
                  <SharedBarChart
                      data={inputTypeBarData}
                      xKey="name"
                      valueKey="value"
                      colors={INPUT_TYPE_COLORS}
                      showLegend={true}
                  />
                </div>
              </div>

              {/* 상위 태그 */}
              <div
                  className={cn(
                      'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
                      'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
                  )}
              >
                <div
                    className="mb-3 flex items-center justify-between text-sm font-medium text-zinc-700 dark:text-zinc-200">
                  <span>상위 태그 Top 5</span>
                  <span className="text-xs text-zinc-500 dark:text-zinc-400">
                가장 많이 등장한 태그
              </span>
                </div>
                <div className="space-y-2 text-xs">
                  {topTags.map(([tag, count], idx) => (
                      <div
                          key={tag}
                          className="flex items-center justify-between gap-3 rounded-xl bg-zinc-50 px-3 py-2 dark:bg-zinc-900/60"
                      >
                        <div className="flex items-center gap-2">
                    <span className="text-[11px] font-semibold text-zinc-500">
                      #{idx + 1}
                    </span>
                          <span className="font-medium">{tag}</span>
                        </div>
                        <span className="text-zinc-500 dark:text-zinc-400">
                    {count}문제
                  </span>
                      </div>
                  ))}
                </div>
              </div>
            </motion.div>
          </motion.section>
        </main>
        <Footer/>
      </>
  );
}
