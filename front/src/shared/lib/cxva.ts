import { type VariantProps, cva } from 'class-variance-authority';
import { cn } from './cn';

export { type VariantProps };

export const cxva = (base: string, config?: Parameters<typeof cva>[1]) => {
  const baseCva = cva(base, config);
  return (...args: Parameters<typeof baseCva>) => {
    return cn(baseCva(...args));
  };
}