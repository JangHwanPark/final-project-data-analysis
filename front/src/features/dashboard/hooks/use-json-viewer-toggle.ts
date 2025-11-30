import { useState, useCallback } from 'react';

export const useJsonViewerToggle = (initialState = false) => {
  const [expanded, setExpanded] = useState(initialState);

  // 토글 핸들러
  const toggle = useCallback(() => {
    setExpanded((prev) => !prev);
  }, []);

  // 명시적으로 열거나 닫을 때 (필요시 사용)
  const open = useCallback(() => setExpanded(true), []);
  const close = useCallback(() => setExpanded(false), []);

  return {
    expanded,
    toggle,
    open,
    close
  };
};