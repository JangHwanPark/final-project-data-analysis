from enum import Enum
from typing import Literal

# ====================================================
# PIPELINE OPTIONS
# ====================================================
# AnalysisScope = Literal["full", "basic", "custom"]
class AnalysisScope(str, Enum):
  FULL = "full"
  BASIC = "basic"
  CUSTOM = "custom"


OutputTarget = Literal["json", "excel", "charts"]
