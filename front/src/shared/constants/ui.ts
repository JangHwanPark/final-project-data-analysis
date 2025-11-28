const Z_INDEX = {
  header: 100,
  sidebar: 90,
  dropdown: 200,
  modal: 1000,
  overlay: 900,
  toast: 1100,
} as const;

const LAYOUT = {
  HEADER_HEIGHT: 64,
  SIDEBAR_WIDTH: 260,
  MOBILE_SIDEBAR_WIDTH: 220,
} as const;

const SPACING = {
  sectionY: 40,
  sectionX: 24,
  cardGap: 16,
} as const;

const BREAKPOINTS = {
  mobile: 480,
  tablet: 768,
  laptop: 1024,
  desktop: 1280,
} as const;

export const UI = {
  Z_INDEX,
  LAYOUT,
  SPACING,
  BREAKPOINTS
}