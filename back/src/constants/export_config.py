
# =================================================================
# 파일명 : [포함할 metrics 키 목록]
# =================================================================
FRONTEND_SPLIT_CONFIG = {
    # 개요 (도메인 객체인 OverviewStats의 필드명 사용)
    "overview.json": [
        "total_questions",
        "days_span",
        "earliest_created_at",
        "latest_created_at",
        "difficulty_distribution",
        "problems_per_day"
    ],

    # 난이도 & 볼륨 상세
    "difficulty_volume.json": [
        "difficulty_distribution", # 중복 허용 (필요하다면)
        "avg_description_length_by_difficulty",
        "avg_test_cases_by_difficulty",
        "problems_per_day",
        "difficulty_over_time"
    ],

    # 태그 & 카테고리
    "tags_categories.json": [
        "algorithm_category_distribution",
        "input_type_distribution",
        "top_tags_distribution"
    ],

    # 구조 & 제약조건
    "structure_constraints.json": [
        "example_count_distribution",
        "test_case_count_distribution",
        "description_length_bucket_distribution",
        "constraints_count_distribution"
    ]
}