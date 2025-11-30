import React from 'react';

export type DashboardTabKey = 'overview' | 'difficulty' | 'tags' | 'structure' | 'raw';

export type HeaderConfig = {
  TITLE: string;
  DESCRIPTION: string;
};

export interface TabItem {
  id: DashboardTabKey;
  label: string;
  icon: React.ElementType;
}