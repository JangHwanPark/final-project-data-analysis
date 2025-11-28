const sleep = (ms: number) =>
  new Promise((resolve) => setTimeout(resolve, ms));

const assertUnreachable(x: never): never => {
  throw new Error(`Unexpected value: ${x}`);
}

export const misc = {
  sleep,
  assertUnreachable
}