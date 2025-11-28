import React from 'react';
import { MESSAGE } from '@/shared/constants';
import Link from 'next/link';

export const Footer = () => {
  return (
      <footer className="mt-auto py-4 text-center">
          <div className="flex flex-col items-center justify-center gap-1">
          <p className="text-[10px] text-zinc-400 dark:text-zinc-600 sm:text-xs">
            Released under the{' '}
            <Link
              href="https://opensource.org/licenses/MIT"
              target="_blank"
              rel="noreferrer"
              className="font-medium underline underline-offset-2 transition-colors hover:text-zinc-600 dark:hover:text-zinc-400"
            >
              MIT License
            </Link>
            .
          </p>
          <p className="text-[10px] text-zinc-400 dark:text-zinc-600 sm:text-xs">
            {MESSAGE.COPYRIGHT}
          </p>
        </div>
      </footer>
  );
};
