const AUTHOR = "Jang-hwan Park";
// const PROJECT_START_YEAR = 2025;
const THIS_YEAR = new Date().getFullYear();
const COPYRIGHT = `© ${THIS_YEAR} ${AUTHOR} Final Project. All rights reserved.`;

const ERROR = {
  UNKNOWN: "알 수 없는 오류가 발생했습니다.",
  NETWORK: "네트워크 연결을 확인해주세요.",
};

const UI_TEXT = {
  EMPTY_LIST: "등록된 데이터가 없습니다.",
  LOADING: "데이터를 불러오는 중입니다...",
};

export const MESSAGE = {
  COPYRIGHT,
  ERROR,
  UI_TEXT
}