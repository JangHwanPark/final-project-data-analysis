const sleep = (ms: number): Promise<void> => {
  return new Promise<void>((resolve) => setTimeout(resolve, ms));
}

const assertUnreachable = (x: never): never => {
  throw new Error(`Unexpected value: ${x}`);
};

export const misc = {
  sleep,
  assertUnreachable
}