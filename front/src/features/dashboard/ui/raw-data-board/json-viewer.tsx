'use client';
import React from 'react';

import { MOTION } from '@/shared/lib';
import { AnimatePresence, motion } from 'framer-motion';
import { Check, ChevronDown, ChevronRight, Copy, Download, FileJson } from 'lucide-react';
import { useRawDataActions } from '@/features/dashboard';

// =================================================================
// 상단 타이틀 + 버튼 영역 (ActionToolbar)
// =================================================================
const ActionToolbar = ({ data }: { data: any }) => {
  const { copied, handleCopy, handleDownload } = useRawDataActions(data);

  return (
    <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex items-center gap-3">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/10 text-blue-500">
          <FileJson className="h-5 w-5" />
        </div>
        <div>
          <h3 className="text-lg font-bold text-white">Raw Data Explorer</h3>
          <p className="text-xs text-zinc-500">
            전체 분석 데이터를 확인하고 다운로드할 수 있습니다.
          </p>
        </div>
      </div>

      <div className="flex gap-2">
        <button
          onClick={handleCopy}
          className="flex items-center gap-2 rounded-lg border border-white/10 bg-zinc-800 px-4 py-2 text-sm font-medium text-zinc-300 transition-all hover:cursor-pointer hover:bg-zinc-700 hover:text-white active:scale-95"
        >
          {copied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4" />}
          {copied ? 'Copied!' : 'Copy JSON'}
        </button>
        <button
          onClick={handleDownload}
          className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-lg shadow-blue-500/20 transition-all hover:cursor-pointer hover:bg-blue-500 active:scale-95"
        >
          <Download className="h-4 w-4" />
          Download File
        </button>
      </div>
    </div>
  );
};

// =================================================================
// 토글 버튼: JSON 펼치기 / 접기 버튼
// =================================================================
interface ToggleProps {
  expanded: boolean;
  onToggle: () => void;
}

const ToggleButton = ({ expanded, onToggle }: ToggleProps) => {
  return (
    <motion.div variants={MOTION.FADEINUP(0.04)} className="flex flex-wrap gap-2">
      <button
        onClick={onToggle}
        className="flex items-center gap-1 rounded-lg border border-white/10 bg-zinc-900 px-3 py-2 text-xs font-medium text-zinc-300 transition-all hover:cursor-pointer hover:bg-zinc-800 hover:text-white active:scale-95"
      >
        {expanded ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
        {expanded ? 'Collapse JSON' : 'Expand JSON'}
      </button>
    </motion.div>
  );
};

// =================================================================
// JSON 뷰어 영역: JSON Preview Area
// =================================================================
interface PreviewProps {
  data: any;
  expanded: boolean;
}

const PreviewArea = ({data, expanded}: PreviewProps) => {
  return (
    <motion.div variants={MOTION.FADEINUP(0.05)} className="group relative mt-4">
      <div className="absolute -inset-0.5 rounded-xl bg-gradient-to-r from-blue-500/20 to-purple-500/20 opacity-0 blur transition duration-500 group-hover:opacity-100" />
      <div className="relative overflow-hidden rounded-xl border border-white/10 bg-[#0d1117] p-4 font-mono text-xs text-zinc-300 shadow-inner">
        <div className="absolute top-0 right-0 z-10 rounded-bl-xl border-b border-l border-white/10 bg-zinc-900 px-3 py-1.5 text-[10px] text-zinc-500">
          {expanded ? 'readonly' : 'collapsed'}
        </div>
        <AnimatePresence>
          {expanded && (
            <motion.div
              key="json-expanded"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 600, opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3 }}
              className="custom-scrollbar overflow-auto pr-2 leading-relaxed"
            >
              <pre className="h-[600px]">{JSON.stringify(data, null, 2)}</pre>
            </motion.div>
          )}
          {!expanded && (
            <motion.div
              key="json-collapsed"
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 96, opacity: 1 }} // h-24 = 96px
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.25 }}
              className="flex items-center justify-center text-[14px] text-zinc-500"
            >
              JSON 뷰가 접혀 있습니다. &quot;Expand JSON&quot;을 눌러 내용을 확인하세요.
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.div>
  );
};

export const JsonViewer = {
  PreviewArea,
  ToggleButton,
  ActionToolbar,
};
