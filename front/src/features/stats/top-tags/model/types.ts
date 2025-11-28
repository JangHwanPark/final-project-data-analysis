export type TopTagItem = {
  rank: number;
  tag: string;
  count: number;
};

export type TopTagsVM = {
  items: TopTagItem[];
};