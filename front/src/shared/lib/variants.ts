import {Variants} from "framer-motion";
import { MOTION } from '@/shared/lib';
// 페이드 인 + 살짝 위에서
const fadeInUp = (delay = 0): Variants => ({
  hidden: { opacity: 0, y: 12 },
  show: {
    opacity: 1,
    y: 0,
    transition: { ...MOTION.EASE_OUT, delay },
  },
});

// 스케일 인
const scaleIn = (delay = 0): Variants => ({
  hidden: { opacity: 0, scale: 0.95 },
  show: {
    opacity: 1,
    scale: 1,
    transition: { ...MOTION.EASE_OUT, delay },
  },
});

// 리스트용 stagger 컨테이너
const staggerContainer = (stagger = 0.06, delayChildren = 0) => ({
  hidden: {},
  show: {
    transition: {
      staggerChildren: stagger,
      delayChildren,
    },
  },
});

export const MOTION_VARIANTS = {
    FADEINUP: fadeInUp,
    SCALEIN: scaleIn,
    STAGGER_CONTAINER: staggerContainer
}