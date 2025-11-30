'use client';

import React, { useState } from 'react';

import { MOTION } from '@/shared/lib/motion';
import { AnimatePresence, motion } from 'framer-motion';
import {
  Check,
  ChevronDown,
  ChevronRight,
  Copy,
  Download,
  FileJson,
} from 'lucide-react';
import { RawData } from '@/features/dashboard/ui/raw-data-board';

interface Props {
  data: any; // 전체 JSON 데이터
}

export const RawDataContent = ({ data }: Props) => {
  const [expanded, setExpanded] = useState(false);

  if (!data) {
    return <div className="p-10 text-center text-zinc-500">데이터를 불러오는 중입니다...</div>;
  }

  return (
    <motion.section
      variants={MOTION.STAGGER_CONTAINER(0.06)}
      initial="hidden"
      animate="show"
      className="flex flex-col gap-6"
    >
      <RawData.Header/>
      <motion.div
        variants={MOTION.FADEINUP(0.02)}
        className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
      >
        {/* 상단 툴바(제목 + 복사/다운로드) */}
        <RawData.JsonViewer.ActionToolbar data={data}/>
        {/* 토글 버튼(props로 상태 전달) */}
        <RawData.JsonViewer.ToggleButton
          expanded={expanded}
          onToggle={() => setExpanded((prev) => !prev)}
        />
        {/* JSON 뷰어 영역(props로 데이터/상태 전달) */}
        <RawData.JsonViewer.PreviewArea
          data={data}
          expanded={expanded}
        />
      </motion.div>
    </motion.section>
  );
};
