import { DataSet } from '@/shared/data/index';

export type JsonDataType = (typeof DataSet)[keyof typeof DataSet];

export interface DataSetItem {
  id: string;
  label: string;
  data: JsonDataType;
}