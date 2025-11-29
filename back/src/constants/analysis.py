# =================================================================
# 문제 분류 및 특징 추출에 사용되는 도메인 상수/키워드 모음
# =================================================================
from __future__ import annotations
from typing import Dict, List, Sequence, Tuple, Type
import re

DEFAULT_NA_VALUE = "Unknown"

# =================================================================
# 알고리즘 카테고리 매핑 (Algorithm Category Mapping)
# =================================================================
ALGORITHM_CATEGORY_KEYWORDS: Dict[str, list[str]] = {
  "Tree": ["tree", "binary tree"],
  "Graph": ["graph", "bfs", "dfs"],
  "DP": ["dynamic programming", "dp"],
  "Greedy": ["greedy"],
  "String": ["string", "substring"],
  "Sliding Window": ["sliding window"],
  "Binary Search": ["binary search"],
  "Heap": ["heap", "priority queue"],
  "Math": ["math", "modulo", "gcd"],
  "Two Pointers": ["two pointers"],
  "Interval": ["interval"],
  "Stack": ["stack"],
  "Queue": ["queue"],
}

# =================================================================
# 입력 타입 매핑 (Input Type Mapping)
# =================================================================
INPUT_TYPE_KEYWORDS: Dict[str, list[str]] = {
  "Array": ["array", "list"],
  "Matrix": ["matrix", "grid"],
  "Tree": ["tree"],
  "Graph": ["graph"],
  "String": ["string"],
}

# =================================================================
# 상세 문제 태그 매핑 (Detailed Problem Tags)
# =================================================================
TAG_KEYWORDS: Dict[str, list[str]] = {
  "array": ["array", "list"],
  "tree": ["tree"],
  "graph": ["graph", "bfs", "dfs"],
  "dp": ["dynamic programming", "dp"],
  "greedy": ["greedy"],
  "string": ["string", "substring"],
  "heap": ["heap", "priority queue"],
  "binary_search": ["binary search"],
  "sliding_window": ["sliding window"],
  "math": ["math", "gcd", "lcm", "mod"],
  "two_pointers": ["two pointers"],
  "matrix": ["matrix", "grid"],
  "interval": ["interval"],
  "stack": ["stack"],
  "queue": ["queue"],
}

# =================================================================
# 출력 타입 매핑 (Output Type Mapping - 런타임 타입 기준)
# =================================================================
OUTPUT_TYPE_MAPPINGS: list[tuple[Type, str]] = [
  (bool, "Boolean"),
  (int, "Integer"),
  (float, "Float"),
  (str, "String"),
  (list, "Array"),
  (dict, "Object"),
]

# =================================================================
# 설명 템플릿 패턴 (Description Template Patterns)
# =================================================================
DESCRIPTION_TEMPLATE_PATTERNS: Dict[str, re.Pattern[str]] = {
  "given_array": re.compile(r"given an array", re.IGNORECASE),
  "given_binary_tree": re.compile(r"given a binary tree", re.IGNORECASE),
  "given_graph": re.compile(r"given a graph", re.IGNORECASE),
  "return_true_false": re.compile(r"return (true|false)", re.IGNORECASE),
}

# =================================================================
# 통계 버킷 설정 (Statistics Buckets for Grouping)
# =================================================================
# 예제 개수 버킷 설정
EXAMPLE_BINS: Sequence[float] = [-0.5, 0.5, 1.5, 2.5, float("inf")]
EXAMPLE_LABELS: list[str] = ["0", "1", "2", "3+"]

# 테스트 케이스 개수 버킷 설정
TEST_CASE_BINS: Sequence[float] = [-0.5, 1.5, 3.5, 6.5, float("inf")]
TEST_CASE_LABELS: list[str] = ["0-1", "2-3", "4-6", "7+"]

# 설명 길이 버킷 설정
DESCRIPTION_LENGTH_BINS: Sequence[float] = [-1, 200, 400, 600, float("inf")]
DESCRIPTION_LENGTH_LABELS: list[str] = ["0-200", "201-400", "401-600", "601+"]

# 제약 조건 개수 버킷 설정
CONSTRAINTS_BINS: Sequence[float] = [-1, 0, 1, 3, float("inf")]
CONSTRAINTS_LABELS: list[str] = ["0", "1", "2-3", "4+"]
