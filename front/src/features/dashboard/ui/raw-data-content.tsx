import React from 'react';

import { RawData } from '@/features/dashboard/ui/raw-data-board';
import { DataSetArray } from '@/shared/data';
import { MOTION } from '@/shared/lib/motion';
import { motion } from 'framer-motion';
import { RawDataItem } from '@/features/dashboard/ui/raw-data-board/raw-data-item';

export const RawDataContent = () => {


  if (!DataSetArray || DataSetArray.length === 0) {
    return <div className="p-10 text-center text-zinc-500">데이터를 불러오는 중입니다...</div>;
  }

  return (
    <motion.section
      variants={MOTION.STAGGER_CONTAINER(0.06)}
      initial="hidden"
      animate="show"
      className="flex flex-col gap-6"
    >
      <RawData.Header />
      {DataSetArray.map(item => (
        <RawDataItem key={item.id} item={item}/>
      ))}
    </motion.section>
  );
};
