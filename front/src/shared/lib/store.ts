import { create } from 'zustand';

const createStore = (...args: any) => {
  // create 함수를 any로 캐스팅하여 타입 검사를 단순화합니다.
  // 실제로는 zustand create의 모든 인자를 전달하고 있습니다.
  return (create as any)(...args);
}

export const store = {
  create: createStore
}