'use client';

import { motion } from 'framer-motion';
import { ArrowUpRight, Activity, BarChart3, ListTodo } from 'lucide-react';
import type {
  DashboardStat,
  ActivityItem,
  SummaryRow,
} from '@/shared/constants/dashboard';
import { MOTION_VARIANTS } from '@/shared/lib/variants';
import { FORMAT } from '@/shared/lib/format';
import { cn } from '@/shared/lib/cn';

type DashboardPageProps = {
  stats: DashboardStat[];
  activities: ActivityItem[];
  summaryRows: SummaryRow[];
};

export const DashboardPage = ({
  stats,
  activities,
  summaryRows,
}: DashboardPageProps) => {
  return (
    <main className="mx-auto flex min-h-screen max-w-6xl flex-col gap-8 px-4 py-8 md:px-8 md:py-10">
      {/* 상단 헤더 */}
      <header className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div className="space-y-2">
          <p className="inline-flex items-center gap-2 rounded-full bg-zinc-100 px-3 py-1 text-xs font-medium text-zinc-600 dark:bg-zinc-900 dark:text-zinc-300">
            <span className="inline-flex h-1.5 w-1.5 rounded-full bg-emerald-500" />
            실시간 테스트 실행 현황
          </p>
          <h1 className="text-2xl font-semibold tracking-tight sm:text-3xl">
            프로젝트 대시보드
          </h1>
          <p className="max-w-xl text-sm text-zinc-600 dark:text-zinc-400">
            테스트 케이스, 실행 성공률, 이슈 현황을 한 페이지에서 빠르게 확인하세요.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button className="inline-flex items-center justify-center gap-2 rounded-full border border-zinc-200 px-4 py-2 text-xs font-medium text-zinc-700 transition hover:bg-zinc-100 dark:border-zinc-800 dark:text-zinc-200 dark:hover:bg-zinc-900">
            <ListTodo className="h-4 w-4" />
            테스트 케이스 관리
          </button>
          <button className="inline-flex items-center justify-center gap-2 rounded-full bg-zinc-900 px-4 py-2 text-xs font-medium text-zinc-50 transition hover:bg-zinc-800 dark:bg-zinc-50 dark:text-zinc-900 dark:hover:bg-zinc-200">
            <BarChart3 className="h-4 w-4" />
            상세 리포트 보기
            <ArrowUpRight className="h-3 w-3" />
          </button>
        </div>
      </header>

      {/* 콘텐츠 그리드 */}
      <motion.section
        variants={MOTION_VARIANTS.STAGGER_CONTAINER(0.06)}
        initial="hidden"
        animate="show"
        className="grid gap-6 md:grid-cols-[1.6fr_1fr]"
      >
        {/* 왼쪽: 카드 + 테이블 */}
        <div className="space-y-6">
          {/* 상단 요약 카드 3개 */}
          <motion.div
            variants={MOTION_VARIANTS.FADEINUP(0.02)}
            className="grid gap-4 sm:grid-cols-3"
          >
            {stats.map((stat) => (
              <div
                key={stat.id}
                className={cn(
                  'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
                  'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
                )}
              >
                <p className="text-xs font-medium text-zinc-500 dark:text-zinc-400">
                  {stat.label}
                </p>
                <p className="mt-2 text-2xl font-semibold tracking-tight">
                  {stat.value}
                </p>
                {stat.subLabel && (
                  <p className="mt-1 text-xs text-zinc-500 dark:text-zinc-400">
                    {stat.subLabel}
                  </p>
                )}
              </div>
            ))}
          </motion.div>

          {/* 하단: 요약 테이블 */}
          <motion.div
            variants={MOTION_VARIANTS.FADEINUP(0.04)}
            className={cn(
              'overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm shadow-zinc-100',
              'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
            )}
          >
            <div className="flex items-center justify-between border-b border-zinc-100 px-4 py-3 text-sm font-medium text-zinc-700 dark:border-zinc-800 dark:text-zinc-200">
              <span>테스트 스위트 요약</span>
              <span className="text-xs text-zinc-500 dark:text-zinc-400">
                최근 7일 기준
              </span>
            </div>
            <div className="divide-y divide-zinc-100 text-sm dark:divide-zinc-800">
              {summaryRows.map((row) => (
                <div
                  key={row.id}
                  className="flex items-center px-4 py-3 hover:bg-zinc-50 dark:hover:bg-zinc-900/60"
                >
                  <div className="flex-1">
                    <p className="font-medium">
                      {FORMAT.truncate(row.name, 22)}
                    </p>
                    <p className="text-xs text-zinc-500 dark:text-zinc-400">
                      총 {row.total}건 실행
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="h-1.5 w-28 overflow-hidden rounded-full bg-zinc-200 dark:bg-zinc-800">
                      <div
                        className="h-full rounded-full bg-emerald-500"
                        style={{ width: `${row.successRate * 100}%` }}
                      />
                    </div>
                    <span className="w-12 text-right text-xs font-medium text-zinc-700 dark:text-zinc-200">
                      {FORMAT.percent(row.successRate, 0)}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* 오른쪽: 액티비티 타임라인 */}
        <motion.aside
          variants={MOTION_VARIANTS.FADEINUP(0.06)}
          className={cn(
            'flex flex-col gap-4 rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
            'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
          )}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-medium text-zinc-800 dark:text-zinc-100">
              <Activity className="h-4 w-4 text-emerald-500" />
              최근 활동
            </div>
            <button className="text-xs text-zinc-500 underline-offset-2 hover:underline dark:text-zinc-400">
              전체 보기
            </button>
          </div>

          <div className="space-y-3">
            {activities.map((item) => (
              <div
                key={item.id}
                className="relative flex gap-3 rounded-xl border border-zinc-100 bg-zinc-50/80 px-3 py-3 text-xs hover:bg-zinc-50 dark:border-zinc-800 dark:bg-zinc-900/60 dark:hover:bg-zinc-900"
              >
                <div className="mt-0.5 h-6 w-6 shrink-0 rounded-full bg-emerald-500/10 text-emerald-500 dark:bg-emerald-500/15">
                  <div className="flex h-full items-center justify-center text-[10px] font-semibold">
                    #
                  </div>
                </div>
                <div className="space-y-0.5">
                  <p className="text-[13px] font-medium text-zinc-800 dark:text-zinc-100">
                    {item.title}
                  </p>
                  <p className="text-[11px] text-zinc-500 dark:text-zinc-400">
                    {item.description}
                  </p>
                  <p className="text-[11px] text-zinc-400 dark:text-zinc-500">
                    {item.time}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </motion.aside>
      </motion.section>
    </main>
  );
}
