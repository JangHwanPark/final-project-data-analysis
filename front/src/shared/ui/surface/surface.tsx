import React from 'react';
import {cn} from "@/shared/lib";

type SurfaceProps = React.HTMLAttributes<HTMLDivElement> & {
  asChild?: boolean;
};

export const Surface = ({className, ...rest}: SurfaceProps) => {
  return (
      <div
          className={cn(
              'rounded-2xl border border-zinc-200 bg-white p-4 shadow-sm shadow-zinc-100',
              'dark:border-zinc-800 dark:bg-zinc-950/60 dark:shadow-none',
              className,
          )}
          {...rest}
      />
  );
};