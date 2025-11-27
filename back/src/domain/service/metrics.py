import pandas as pd


def total_questions(df) -> int:
  return int(len(df))


def difficulty_counts(df) -> dict:
  return df["difficulty"].value_counts().to_dict()


def tag_counts(df) -> dict:
  tags = (
    df["tags"]
    .dropna()
    .str.split(",")
    .explode()
    .str.strip()
  )
  return tags.value_counts().to_dict()


def compute_statistics(df: pd.DataFrame) -> dict:
  # 데이터셋 통계 계산 -> return dict
  stats: dict = {}

  # 전체 문제 수
  stats['total_questions'] = int(len(df))

  # 난이도 별 분포
  if "difficulty" in df.columns:
    # value_counts() 패턴 잘 익혀두기
    difficulty_counts = df["difficulty"].value_counts().to_dict()
    stats["difficulty_counts"] = difficulty_counts

  # 태그(콤마로 묶여있다면 explode 패턴)
  if "tags" in df.columns:
    # "array,string" 이런 식이라면
    # split → explode 후 value_counts
    tag_series = (
      df["tags"]
      .dropna()
      .str.split(",")  # ["array", "string"]
      .explode()  # 한 행씩 분리
      .str.strip()
    )
    stats["tag_counts"] = tag_series.value_counts().to_dict()

  return stats
