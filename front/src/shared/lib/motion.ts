import type { Transition, Variants } from 'framer-motion';







const TRANSITION: Transition = {
  type: 'spring',
  stiffness: 260,
  damping: 20,
};

const EASE_OUT: Transition = {
  type: 'tween',
  ease: 'easeOut',
  duration: 0.3,
};

const STAGGER_CONTAINER = (staggerChildren = 0.1): Variants => ({
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren,
    },
  },
});

const FADEINUP = (delay = 0): Variants => ({
  hidden: { opacity: 0, y: 20 },
  show: {
    opacity: 1,
    y: 0,
    transition: {
      type: 'spring',
      duration: 0.5,
      delay,
    },
  },
});

export const MOTION = {
  STAGGER_CONTAINER,
  TRANSITION,
  EASE_OUT,
  FADEINUP,
};
