'use client';

import type { ReactNode } from 'react';
import { cn } from '@/shared/lib';

/* Root */
type PageHeaderRootProps = {
  children: ReactNode;
  className?: string;
};

const PageHeaderRoot = ({ children, className }: PageHeaderRootProps) => {
  return (
    <header
      className={cn(
        'flex flex-col gap-3 md:flex-row md:items-end md:justify-between',
        className,
      )}
    >
      {children}
    </header>
  );
};

/* Main */
type PageHeaderMainProps = {
  children: ReactNode;
  className?: string;
};

const PageHeaderMain = ({ children, className }: PageHeaderMainProps) => {
  return <div className={cn('space-y-2', className)}>{children}</div>;
};

/* Badge */
type PageHeaderBadgeProps = {
  children: ReactNode;
  className?: string;
};

const PageHeaderBadge = ({ children, className }: PageHeaderBadgeProps) => {
  return (
    <p
      className={cn(
        'inline-flex items-center gap-2 rounded-full bg-zinc-100 px-3 py-1 text-xs font-medium text-zinc-600',
        'dark:bg-zinc-900 dark:text-zinc-300',
        className,
      )}
    >
      {children}
    </p>
  );
};

/* Title */
type PageHeaderTitleProps = {
  children: ReactNode;
  className?: string;
};

const PageHeaderTitle = ({ children, className }: PageHeaderTitleProps) => {
  return (
    <h1
      className={cn(
        'text-2xl font-semibold tracking-tight sm:text-3xl',
        className,
      )}
    >
      {children}
    </h1>
  );
};

/* Description */
type PageHeaderDescriptionProps = {
  children: ReactNode;
  className?: string;
};

const PageHeaderDescription = ({
  children,
  className,
}: PageHeaderDescriptionProps) => {
  return (
    <p
      className={cn(
        'max-w-xl text-sm text-zinc-600 dark:text-zinc-400',
        className,
      )}
    >
      {children}
    </p>
  );
};

/* Meta */
type PageHeaderMetaProps = {
  children: ReactNode;
  className?: string;
};

const PageHeaderMeta = ({ children, className }: PageHeaderMetaProps) => {
  return (
    <div className={cn('text-xs text-zinc-500 dark:text-zinc-400', className)}>
      {children}
    </div>
  );
};

/* MetaValue */
type PageHeaderMetaValueProps = {
  children: ReactNode;
  className?: string;
};

const PageHeaderMetaValue = ({
  children,
  className,
}: PageHeaderMetaValueProps) => {
  return (
    <span
      className={cn(
        'font-medium text-zinc-700 dark:text-zinc-200',
        className,
      )}
    >
      {children}
    </span>
  );
};

/* Export API */
export const PageHeader = {
  Root: PageHeaderRoot,
  Main: PageHeaderMain,
  Badge: PageHeaderBadge,
  Title: PageHeaderTitle,
  Description: PageHeaderDescription,
  Meta: PageHeaderMeta,
  MetaValue: PageHeaderMetaValue,
};
