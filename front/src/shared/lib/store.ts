import { create } from 'zustand';

type CreateStore = typeof create;

const create: CreateStore = (...args: any) => create(...(args as any));

export const store = {
  create
}