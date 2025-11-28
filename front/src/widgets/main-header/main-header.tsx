'use client';

import { PageHeader } from '@/shared/ui/page-header';

type MainHeaderProps = {
  badgeText: string;
  title: string;
  description?: string;
  metaLabel?: string;
  metaValue?: string;
};

export const MainHeader = ({
  badgeText,
  title,
  description,
  metaLabel,
  metaValue,
}: MainHeaderProps) => {
  return (
    <PageHeader.Root>
      <PageHeader.Main>
        <PageHeader.Badge>
          <span className="inline-flex h-1.5 w-1.5 rounded-full bg-emerald-500" />
          {badgeText}
        </PageHeader.Badge>

        <PageHeader.Title>{title}</PageHeader.Title>

        {description && (
          <PageHeader.Description>{description}</PageHeader.Description>
        )}
      </PageHeader.Main>

      {(metaLabel || metaValue) && (
        <PageHeader.Meta>
          {metaLabel}{' '}
          {metaValue && (
            <PageHeader.MetaValue>{metaValue}</PageHeader.MetaValue>
          )}
        </PageHeader.Meta>
      )}
    </PageHeader.Root>
  );
};