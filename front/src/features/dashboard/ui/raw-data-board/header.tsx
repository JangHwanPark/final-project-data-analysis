import React from 'react';
import { MOTION } from '@/shared/lib';
import Link from 'next/link';
import { ExternalLink } from 'lucide-react';
import { motion } from 'framer-motion';

const DATASET_URL = 'https://www.kaggle.com/datasets/guitaristboy/coding-questions-dataset';

export const Header = () => {
  return (
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
  );
};