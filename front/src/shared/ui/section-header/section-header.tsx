import React from 'react';
import {cn} from '@/shared/lib';

type SectionHeaderProps = {
  title: string;
  right?: string | React.ReactNode;
  className?: string;
};

export function SectionHeader({title, right, className}: SectionHeaderProps) {
  return (
      <div
          className={cn(
              "mb-3 flex items-center justify-between text-sm font-medium text-zinc-700 dark:text-zinc-200",
              className
          )}
      >
        <span>{title}</span>
        {right && (
            <span className="text-xs text-zinc-500 dark:text-zinc-400">
          {right}
        </span>
        )}
      </div>
  );
}
