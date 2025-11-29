from typing import Final, List

# 기본 설정
ENCODING: Final[str] = "utf-8"

# CSV 로딩 시 날짜로 파싱할 컬럼(Data Loader에서 필요)
DATE_COLUMNS: Final[List[str]] = ["created_at", "updated_at", "CreatedAt"]