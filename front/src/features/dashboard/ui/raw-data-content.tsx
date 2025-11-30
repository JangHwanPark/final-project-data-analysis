'use client';

import React, { useState } from 'react';

import Link from 'next/link';

import { MOTION } from '@/shared/lib/motion';
import { AnimatePresence, motion } from 'framer-motion';
import {
  Check,
  ChevronDown,
  ChevronRight,
  Copy,
  Download,
  ExternalLink,
  FileJson,
} from 'lucide-react';

interface Props {
  data: any; // 전체 JSON 데이터
}

const DATASET_URL = 'https://www.kaggle.com/datasets/guitaristboy/coding-questions-dataset';

export const RawDataContent = ({ data }: Props) => {
  const [copied, setCopied] = useState(false);
  const [expanded, setExpanded] = useState(true);

  // 클립보드 복사 핸들러
  const handleCopy = () => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // 파일 다운로드 핸들러
  const handleDownload = () => {
    const jsonString = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const link = document.createElement('a');
    link.href = url;
    link.download = `analysis_summary_${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

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
      <motion.div
        variants={MOTION.FADEINUP(0.01)}
        className="rounded-2xl border border-blue-500/30 bg-blue-500/5 p-4 text-xs text-zinc-300"
      >
        <div className="mb-1 text-[16px] font-semibold tracking-wide text-blue-300 uppercase">
          Data Source &amp; License
        </div>
        <p className="mb-2 text-[14px] text-zinc-400">
          이 분석은 Kaggle 공개 데이터셋을 기반으로 합니다. 상업적 사용 또는 2차 배포 시에는 원
          데이터셋 페이지의 라이선스 및 이용 약관을 반드시 확인하세요.
        </p>
        <Link
          href={DATASET_URL}
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-1 rounded-lg border border-blue-500/50 bg-blue-500/10 px-3 py-1.5 text-[11px] font-medium text-blue-200 transition-colors hover:bg-blue-500/20"
        >
          <ExternalLink className="h-3 w-3" />
          View original dataset on Kaggle
        </Link>
      </motion.div>
      <motion.div
        variants={MOTION.FADEINUP(0.02)}
        className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
      >
        {/* 상단 타이틀 + 버튼 영역 */}
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

        {/* JSON Preview Area */}
        <motion.div variants={MOTION.FADEINUP(0.04)} className="flex flex-wrap gap-2">
          {/* JSON 펼치기/접기 */}
          <button
            onClick={() => setExpanded((prev) => !prev)}
            className="flex items-center gap-1 rounded-lg border border-white/10 bg-zinc-900 px-3 py-2 text-xs font-medium text-zinc-300 transition-all hover:cursor-pointer hover:bg-zinc-800 hover:text-white active:scale-95"
          >
            {expanded ? <ChevronDown className="h-3 w-3" /> : <ChevronRight className="h-3 w-3" />}
            {expanded ? 'Collapse JSON' : 'Expand JSON'}
          </button>
        </motion.div>

        {/* JSON Preview Area */}
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
                  className="flex items-center justify-center text-[11px] text-zinc-500"
                >
                  JSON 뷰가 접혀 있습니다. &quot;Expand JSON&quot;을 눌러 내용을 확인하세요.
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </motion.div>
    </motion.section>
  );
};
