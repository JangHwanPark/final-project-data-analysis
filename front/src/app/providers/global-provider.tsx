import React from 'react';
import { MantineProvider } from '@mantine/core';

export const GlobalProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <MantineProvider>
      {children}
    </MantineProvider>
  );
};