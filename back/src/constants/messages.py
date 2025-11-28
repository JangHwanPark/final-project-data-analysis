# 파이프라인 배너/타이틀 관련
PIPELINE_VERSION = "3.0"
PIPELINE_TITLE_START = "PYTHON DATA ANALYSIS PIPELINE STARTED (Ver {PIPLINE_VERSION})"
PIPELINE_TITLE_COMPLETE = "PIPELINE EXECUTION COMPLETE (Artifacts Summary)"
PIPELINE_TITLE_FINISHED = "PIPELINE FINISHED"
PIPELINE_TITLE_FAILED = "PIPELINE FAILED"

# 파이프라인 상태/로그 메시지
PIPELINE_INTERACTIVE_ENABLED = "INTERACTIVE MODE ENABLED"
PIPELINE_MESSAGE_FATAL_EMPTY_DATA = "FATAL: Data loading failed or resulted in empty DataFrame. Exiting pipeline."
PIPELINE_ERROR_MESSAGE = "Pipeline failed due to an unexpected error."

# 디렉토리/아티팩트 관련

# 단계별 스텝
PIPELINE_STEP_ENSURE_DIRS = "Ensuring artifact directories..."
PIPELINE_STEP_LOADING_DATA = "Loading data from: {path}"
PIPELINE_STEP_COMPUTE_STATS = "Computing domain metrics and statistics..."
PIPELINE_STEP_GENERATE_CHARTS = "Generating charts and visualizations..."
PIPELINE_STEP_SAVE_ARTIFACTS = "Saving final artifacts across environments..."
PIPELINE_STEP_WRITE_JSON = "Writing primary JSON artifact to {target}....."

# 로그 요약 메세지
PIPELINE_LOG_SAVED = "{label} JSON saved to: {path}"