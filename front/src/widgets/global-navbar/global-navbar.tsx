import Link from 'next/link';
import {Github} from 'lucide-react';
import {LINKS} from '@/shared/constants';

export const GlobalNavbar = () => {
  return (
      <header
          className="w-full border-b border-zinc-200 bg-white/80 backdrop-blur dark:border-zinc-800 dark:bg-zinc-950/70">
        <div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4 md:px-8">

          <Link href="/" className="text-lg font-semibold tracking-tight">
            {LINKS.GNB.LOGO}
          </Link>

          <div className="flex items-center gap-4">
            <Link
                href={LINKS.GNB.GITHUB}
                target="_blank"
                className="flex items-center gap-1 text-sm text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white transition"
            >
              <Github className="h-4 w-4"/>
              GitHub
            </Link>

            <Link
                href={LINKS.GNB.PORTFOLIO}
                target="_blank"
                className="text-sm text-zinc-600 hover:text-zinc-900 dark:text-zinc-400 dark:hover:text-white transition"
            >
              Portfolio
            </Link>
          </div>

        </div>
      </header>
  );
}
