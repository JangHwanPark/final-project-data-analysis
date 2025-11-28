const APP_COLORS = {
  primary: 'indigo',
  danger: 'red',
  success: 'teal',
} as const;

const APP_RADIUS = {
  sm: 'sm',
  md: 'md',
  lg: 'lg',
  pill: 'xl',
} as const;

const APP_SPACING = {
  sectionY: 32,
  sectionX: 24,
} as const;

const MANTINE = {
    APP_COLORS, APP_RADIUS, APP_SPACING
}

export const THEME = {
    MANTINE}