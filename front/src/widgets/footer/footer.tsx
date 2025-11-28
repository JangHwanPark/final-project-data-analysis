import React from 'react';
import {MESSAGE} from "@/shared/constants";

export const Footer = () => {
  return (
      <footer className="mt-auto py-4 text-center">
        <p className="text-[10px] text-zinc-400 dark:text-zinc-600 sm:text-xs">
          {MESSAGE.COPYRIGHT}
        </p>
      </footer>
  );
};
