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

export const MOTION = {
  TRANSITION,
  EASE_OUT
}