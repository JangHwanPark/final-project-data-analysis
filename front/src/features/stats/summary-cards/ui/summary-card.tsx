'use client';
import { motion } from 'framer-motion';
import type { StatsSummary } from '@/entities/summary/types';
import { cn, MOTION_VARIANTS } from '@/shared/lib';
import { buildSummaryCards } from '@/features/stats/summary-cards/model';

type Props = {
  stats: StatsSummary;
};

export function SummaryCards({ stats }: Props) {
  const cards = buildSummaryCards(stats);

  return (
    <motion.div
      variants={MOTION_VARIANTS.FADEINUP(0.02)}
      className="grid gap-4 sm:grid-cols-3"
    >
      {cards.map((card) => (
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
  );
}
