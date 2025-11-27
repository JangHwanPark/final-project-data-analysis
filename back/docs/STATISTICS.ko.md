# STATISTICS
> Online Judge / Problem Bank 통계 설계 문서  
> 데이터를 어떻게 집계해서 어떤 차트로 보여줄지 정의합니다.

---

## 0. 데이터 소스 정의
- **Table**: `problems`
- **주요 컬럼**
  - `id`
  - `title`
  - `description`
  - `difficulty_level` (`Easy | Medium | Hard`)
  - `created_at`, `updated_at`
  - `examples` (JSON 배열)
  - `constraints` (JSON 배열 / 문자열)
  - `test_cases` (JSON 배열)
- **파생 정보 (Derived fields)** — 분석 시 계산
  - `description_length`
  - `num_examples`
  - `num_test_cases`
  - `problem_tags` (description / title 기반 키워드 태깅)
  - `input_types` (array / tree / graph / string / matrix / 기타)

---

## 1. 난이도(Difficulty) 관련 통계
### 1.1 난이도 분포 (Difficulty Distribution)
- **Metric ID**: `difficulty_distribution`
- **설명**: Easy / Medium / Hard 문제 비율
- **집계 방식**
  - `COUNT(*)` 그룹 by `difficulty_level`
- **차트**
  - ✅ Donut / Pie chart (메인 난이도 분포)
  - Bar chart (난이도별 문제 수 비교)

### 1.2 난이도별 평균 설명 길이
- **Metric ID**: `avg_description_length_by_difficulty`
- **설명**: 난이도별 `description_length` 평균
- **집계 방식**
  - `AVG(description_length)` 그룹 by `difficulty_level`
- **차트**
  - Bar chart (Easy vs Medium vs Hard)

### 1.3 난이도별 테스트케이스 수 평균
- **Metric ID**: `avg_test_cases_by_difficulty`
- **설명**: 난이도별 `num_test_cases` 평균
- **차트**
  - Bar chart

---

## 2. 문제 유형 / 알고리즘 카테고리 통계
> description, title, constraints를 기반으로 자동 태깅한 `problem_tags`, `algorithm_category`, `input_types` 사용

### 2.1 알고리즘 카테고리 분포
- **Metric ID**: `algorithm_category_distribution`
- **설명**: 문제를 다음 카테고리로 분류 후 비율/개수 집계
  - `Tree`, `Graph`, `DP`, `Greedy`, `String`,  
    `Sliding Window`, `Binary Search`, `Heap`, `Math`, `Two Pointers`, etc.
- **집계 방식**
  - 태그 기반 1차 분류, `COUNT(*)` 그룹 by `algorithm_category`
- **차트**
  - Donut / Pie (비율)
  - Horizontal bar (카테고리가 많으면)

### 2.2 입력 구조 타입 분포 (Input Type Distribution)
- **Metric ID**: `input_type_distribution`
- **설명**: 문제에서 사용하는 대표 입력 구조 비율
  - `Array`, `Matrix`, `Tree`, `Graph`, `String`, `Mixed` 등
- **차트**
  - Donut / Pie chart

### 2.3 태그 상위 N개 분포
- **Metric ID**: `top_tags_distribution`
- **설명**: `problem_tags` 기준 상위 5~10개 태그 출현 비율
- **차트**
  - Donut / Pie (Top 5)
  - Bar chart (Top 10)

---

## 3. 예시 / 테스트 케이스 관련 통계
### 3.1 예시(Examples) 개수 분포
- **Metric ID**: `example_count_distribution`
- **설명**: `examples` 배열 길이 기반 분포
  - 1개, 2개, 3개 이상 등 구간별 개수
- **차트**
  - Donut / Pie chart
  - Table (정확 숫자 표시용)

### 3.2 테스트 케이스(Test Cases) 개수 분포
- **Metric ID**: `test_case_count_distribution`
- **설명**: `test_cases` 배열 길이 기준 구간 분포
  - 1~2개, 3~5개, 6개 이상 등
- **차트**
  - Donut / Pie chart

### 3.3 난이도별 평균 예시/테스트케이스 수
- **Metric ID**: `example_testcase_by_difficulty`
- **설명**: 난이도별로
  - `avg(num_examples)`
  - `avg(num_test_cases)`
- **차트**
  - Grouped bar chart (난이도 x {examples, test_cases})

---

## 4. 텍스트 길이 / 문제 설명 품질 통계
### 4.1 설명 길이 구간 분포
- **Metric ID**: `description_length_bucket_distribution`
- **설명**: `description_length`를 구간으로 나눈 분포
  - 0–200, 201–400, 401–600, 601+ 등
- **차트**
  - Donut / Pie chart (구간 4~5개)
  - Histogram 스타일 bar chart

### 4.2 제약사항(Constraints) 개수 분포
- **Metric ID**: `constraints_count_distribution`
- **설명**: `constraints` 배열 길이 기준 구간 분포
- **차트**
  - Donut / Pie chart

---

## 5. 시간 축(작성 일자) 기반 통계
### 5.1 날짜별 문제 수 (Time Series)
- **Metric ID**: `problems_per_day`
- **설명**: `created_at` 기준 날짜별 문제 생성 개수
- **차트**
  - Line chart
  - Bar chart (Day/Month 기준)

### 5.2 날짜별 난이도 분포
- **Metric ID**: `difficulty_over_time`
- **설명**: 날짜 단위로 난이도별 개수
- **차트**
  - Stacked bar chart (X축: 날짜, Y축: 문제 수, 색: 난이도)

---

## 6. 입출력/답안 특성 관련 통계

### 6.1 Output 타입 분포
- **Metric ID**: `output_type_distribution`
- **설명**: 정답 형태별 비율
  - Boolean(0/1), Integer, Index, String, Path/Array 등
- **차트**
  - Donut / Pie chart

### 6.2 -1(불가능/없음) 반환 문제 비율
- **Metric ID**: `negative_one_output_problems_ratio`
- **설명**: 가능한 해답이 없는 경우 `-1`을 반환하는 설계의 문제 비율
- **차트**
  - Donut / Pie chart
    - `returns_negative_one`: yes / no

---

## 7. 난이도 × 카테고리 교차 통계
### 7.1 난이도별 카테고리 분포 (Matrix)
- **Metric ID**: `difficulty_algorithm_matrix`
- **설명**: 난이도(Easy/Medium/Hard) × 알고리즘 카테고리(Tree/Graph/DP/…) 개수 매트릭스
- **차트**
  - Heatmap
  - Pivot-style table

### 7.2 난이도별 입력 타입 분포
- **Metric ID**: `difficulty_input_type_matrix`
- **설명**: 난이도 × Input Type(Array, Tree, Graph, …)  
- **차트**
  - Stacked bar chart 또는 Heatmap

---

## 8. 데이터 품질 / 중복 체크 통계
### 8.1 제목 중복/유사도 체크
- **Metric ID**: `duplicate_title_count`
- **설명**: 같은 제목, 매우 유사한 제목이 있는지 여부 (데이터셋 품질용)
- **차트**
  - Table / 카드 형태 (차트보다는 리포트)

### 8.2 description 템플릿 패턴 비율
- **Metric ID**: `description_template_usage`
- **설명**: 자주 쓰이는 문장 패턴(“Given an array…”, “Given a binary tree…”) 비율
- **차트**
  - Donut / Pie chart

---

## 9. 대시보드 구상 (조합)
> 실제 UI에서는 아래처럼 묶어서 하나의 Dashboard로 보여주는 것을 목표로 함.

1. **Overview 섹션**
   - `difficulty_distribution` (Donut)
   - `algorithm_category_distribution` (Donut)
   - `input_type_distribution` (Donut)
2. **Text & Examples 섹션**
   - `description_length_bucket_distribution` (Bar/Donut)
   - `example_count_distribution` (Donut)
   - `test_case_count_distribution` (Donut)
3. **Time Series 섹션**
   - `problems_per_day` (Line)
   - `difficulty_over_time` (Stacked bar)
4. **Cross Analysis 섹션**
   - `difficulty_algorithm_matrix` (Heatmap)
   - `difficulty_input_type_matrix` (Heatmap)
5. **Quality 섹션**
   - `negative_one_output_problems_ratio` (Donut)
   - `duplicate_title_count` (Table)

---

## 10. 구현 시 공통 규칙
- **모든 Metric은 고유 ID(위에서 정의한 `snake_case`)로 관리**
  - Backend: `compute_statistics.py` / `domain.service.metrics` 에서 Metric ID 기준으로 함수 분리
  - Frontend: Chart 컴포넌트에 `metricId` 전달 → API 응답 매핑
- **단위**
  - 기본: `count`, `ratio(%)`, `avg` 명시
- **차트 타입**
  - 파이/도넛: 비율, 구간 분포
  - 바/스택 바: 카테고리 간 비교
  - 라인: 시간 흐름
  - 히트맵: 교차표(난이도 × 카테고리)

---
