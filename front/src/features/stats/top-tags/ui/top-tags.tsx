'use client';

import {SectionHeader} from '@/shared';
import {cn} from '@/shared/lib';
import type {TopTagsVM} from '../model';

type Props = {
  vm: TopTagsVM;
};

export function TopTags({vm}: Props) {
  return (
    <div
      className={cn(
        'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
        'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
      )}
    >
      <SectionHeader title="상위 태그 Top 5" right="가장 많이 등장한 태그"/>
      <div className="space-y-2 text-xs">
        {vm.items.map((item) => (
          <div
            key={item.tag}
            className="flex items-center justify-between gap-3 rounded-xl bg-zinc-50 px-3 py-2 dark:bg-zinc-900/60"
          >
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-semibold text-zinc-500">
                #{item.rank}
              </span>
              <span className="font-medium">{item.tag}</span>
            </div>
            <span className="text-zinc-500 dark:text-zinc-400">
              {item.count}문제
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
