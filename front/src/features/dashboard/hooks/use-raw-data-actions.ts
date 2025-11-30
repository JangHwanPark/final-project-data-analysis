"use client";
import { useState, useCallback } from 'react';

export const useRawDataActions = (data: any) => {
  const [copied, setCopied] = useState(false);

  // 클립보드 복사 핸들러
  const handleCopy = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(data, null, 2));
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  }, [data]);

  // 파일 다운로드 핸들러
  const handleDownload = useCallback(() => {
    try {
      const jsonString = JSON.stringify(data, null, 2);
      const blob = new Blob([jsonString], { type: 'application/json' });
      const url = URL.createObjectURL(blob);

      const link = document.createElement('a');
      link.href = url;
      // 파일명에 날짜를 포함시켜 유니크하게 만듭니다.
      link.download = `analysis_summary_${new Date().toISOString().split('T')[0]}.json`;

      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Failed to download:', err);
    }
  }, [data]);

  return { copied, handleCopy, handleDownload };
};