from .base import DataLoadEngine
from .csv_engine import CSVDataEngine
from .json_engine import JSONDataEngine
# from .db_engine import DBDataEngine


def get_engine(engine: str = "csv") -> DataLoadEngine:
  if engine == "csv":
    return CSVDataEngine()
  if engine == "json":
    return JSONDataEngine()
  # if engine == "db": ...
  raise ValueError(f"Unknown engine: {engine}")
