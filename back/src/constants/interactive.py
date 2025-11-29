from questionary import Choice

# =======================================================================
# Output Targets (checkbox UI)
# =======================================================================
OUTPUT_TARGET_CHOICES = [
    Choice("JSON", checked=True),
    Choice("Excel", checked=True),
    Choice("Charts (images)", checked=False),
]

OUTPUT_TARGET_JSON = "json"
OUTPUT_TARGET_EXCEL = "excel"
OUTPUT_TARGET_CHARTS = "charts"

# 표시 문자열 → 내부 값 맵핑
OUTPUT_TARGET_MAP = {
    "JSON": OUTPUT_TARGET_JSON,
    "Excel": OUTPUT_TARGET_EXCEL,
    "Charts (images)": OUTPUT_TARGET_CHARTS,
}

# =======================================================================
# Analysis Scope
# =======================================================================
ANALYSIS_SCOPE_CHOICES = [
    "Full Analysis (full)",
    "Essential Summary (basic)",
    "Custom Selection (custom)",
]

ANALYSIS_SCOPE_DEFAULT = "Full Analysis (full)"

ANALYSIS_SCOPE_FULL = "full"
ANALYSIS_SCOPE_BASIC = "basic"
ANALYSIS_SCOPE_CUSTOM = "custom"

ANALYSIS_SCOPE_MAP = {
    "Full Analysis (full)": ANALYSIS_SCOPE_FULL,
    "Essential Summary (basic)": ANALYSIS_SCOPE_BASIC,
    "Custom Selection (custom)": ANALYSIS_SCOPE_CUSTOM,
}

# =======================================================================
# Engine Choices (CSV / JSON / DB)
# =======================================================================
ENGINE_CHOICES = [
    "CSV (csv)",
    "JSON (json)",
    "Database (db)",
]

ENGINE_DEFAULT = "CSV (csv)"

ENGINE_MAP = {
    "CSV (csv)": "csv",
    "JSON (json)": "json",
    "Database (db)": "db",
}