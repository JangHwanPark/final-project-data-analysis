// 문자열 자르기 (… 붙이기)
const truncate = (value: string, maxLength: number) => value.length <= maxLength ? value : `${value.slice(0, maxLength)}…`;

// 0.1234 -> "12.34%"
const percent = (value: number, digits = 0) => `${(value * 100).toFixed(digits)}%`;

export const format = {
  truncate,
  percent
}
