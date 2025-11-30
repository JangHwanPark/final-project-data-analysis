[EN](README.md) |  [KO](docs/README.ko.md)

# Backend – Python Data Analysis Pipeline
This backend loads the Kaggle Coding Questions dataset, performs preprocessing, computes statistical metrics, and emits JSON/Excel/chart artifacts for the frontend dashboard. The codebase is organized as a Python package (`backend`) inside `back/src`.

The layered architecture remains the same (app → domain → infrastructure → presentation) but is grouped under a single package root.

## Backend Structure Overview
```text
back/
├─ data/                     # Input CSV file(s)
├─ artifacts/                # Generated JSON files, charts, Excel exports
│   ├─ charts/
│   ├─ json/
│   ├─ summaries/
│   └─ xlsx/
└─ src/                      # Package root (import as `backend`)
   ├─ app/                   # CLI entry point, pipeline orchestration
   ├─ domain/                # Analysis logic & entities
   ├─ infrastructure/        # File I/O, logging, configuration
   └─ presentation/          # Exporters for JSON/Excel/Charts
```

## Dependencies
This project uses the following Python dependencies

| Package       | Version | Purpose |
|---------------|---------|---------|
| **pandas**    | latest  | Data loading, cleaning, transformation, analysis |
| **openpyxl**  | latest  | Reading/writing Excel (.xlsx) files |
| **matplotlib**| latest  | Plotting charts and visualizing analysis results |
| **seaborn**   | latest  | Enhanced statistical data visualization |
| **jupyter**   | latest  | Notebook environment for interactive analysis |

## Installation
### Move into backend directory
```bash
cd back
```

### Create virtual environment
```bash
py -3 -m venv .venv
```

### Activate virtual environment (Windows PowerShell)
```bash
.\.venv\Scripts\activate
```

## Install all dependencies
With the virtual environment activated, run one of the following commands.

```bash
pip install -r requirements.txt
```

OR

```bash
py -3 -m pip install -r requirements.txt
```

OR

```bash
python -m pip install -r requirements.txt
```

### If Python is not recognized
Use the full path inside the virtual environment
```bash
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## How to Run
Run the pipeline from the `back` directory with the `src` folder on your `PYTHONPATH`.
```bash
# Move into backend directory
cd back
# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\activate
python -m src.app.main --data-file data/coding-questions-dataset/questions_dataset.csv
```
The `--data-file` flag is optional; by default the loader reads the CSV defined in `backend.infrastructure.config.DATA_FILE`.

## Artifacts
All analysis results are stored in the following directories. The pipeline also mirrors tabbed JSON files to `front/src/shared/data` for the Next.js app.

```text
artifacts/
  ├─ summaries/   # Statistical summaries, CSV/Excel exports
  ├─ charts/      # Visualization images (plots, graphs)
  ├─ json/        # Tabbed JSON (overview/difficulty/tags/structure/raw)
  └─ xlsx/        # Excel splits per tab
```