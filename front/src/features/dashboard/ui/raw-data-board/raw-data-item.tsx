"use client";
import React from 'react';
import { MOTION } from '@/shared/lib';
import { RawData } from '@/features/dashboard/ui/raw-data-board/index';
import { motion } from 'framer-motion';
import { useJsonViewerToggle } from '@/features/dashboard';
import type { DataSetItem } from '@/shared/data';

interface RawDataItemProps {
  item: DataSetItem;
}

export const RawDataItem = ({item}: RawDataItemProps) => {
  const { expanded, toggle } = useJsonViewerToggle(false);

  return (
    <>
      <motion.div
          variants={MOTION.FADEINUP(0.02)}
          className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
        >
          {/* 상단 툴바(제목 + 복사/다운로드) */}
          <RawData.JsonViewer.ActionToolbar data={item} title={item.label}/>
          {/* 토글 버튼(props로 상태 전달) */}
          <RawData.JsonViewer.ToggleButton
            expanded={expanded}
            onToggle={toggle}
          />
          {/* JSON 뷰어 영역(props로 데이터/상태 전달) */}
          <RawData.JsonViewer.PreviewArea data={item} expanded={expanded} />
        </motion.div>
    </>
  );
};