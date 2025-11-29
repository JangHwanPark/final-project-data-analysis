'use client';

import React, { useState } from 'react';

import { MOTION } from '@/shared/lib/motion';
import { motion } from 'framer-motion';
import { Check, Copy, Download, FileJson } from 'lucide-react';

interface Props {
  data: any; // 전체 JSON 데이터
}

export const RawDataContent = ({ data }: Props) => {
  const [copied, setCopied] = useState(false);

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
        variants={MOTION.FADEINUP(0.02)}
        className="rounded-3xl border border-white/10 bg-zinc-900/30 p-6"
      >
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
              className="flex items-center gap-2 rounded-lg border border-white/10 bg-zinc-800 px-4 py-2 text-sm font-medium text-zinc-300 transition-all hover:bg-zinc-700 hover:text-white active:scale-95"
            >
              {copied ? <Check className="h-4 w-4 text-green-500" /> : <Copy className="h-4 w-4" />}
              {copied ? 'Copied!' : 'Copy JSON'}
            </button>
            <button
              onClick={handleDownload}
              className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-lg shadow-blue-500/20 transition-all hover:bg-blue-500 active:scale-95"
            >
              <Download className="h-4 w-4" />
              Download File
            </button>
          </div>
        </div>

        {/* JSON Preview Area */}
        <div className="group relative">
          <div className="absolute -inset-0.5 rounded-xl bg-gradient-to-r from-blue-500/20 to-purple-500/20 opacity-0 blur transition duration-500 group-hover:opacity-100" />
          <div className="relative overflow-hidden rounded-xl border border-white/10 bg-[#0d1117] p-4 font-mono text-xs text-zinc-300 shadow-inner">
            <div className="absolute top-0 right-0 z-10 rounded-bl-xl border-b border-l border-white/10 bg-zinc-900 px-3 py-1.5 text-[10px] text-zinc-500">
              readonly
            </div>
            <div className="custom-scrollbar h-[600px] overflow-auto pr-2 leading-relaxed">
              <pre>{JSON.stringify(data, null, 2)}</pre>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.section>
  );
}
