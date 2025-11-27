[EN](README.md) |  [KO](docs/README.ko.md)

# Backend – Python Data Analysis Pipeline
This backend module is responsible for loading CSV data, preprocessing it,  
computing statistical metrics, and generating structured JSON artifacts.  
These JSON files are then consumed by the frontend (Next.js) to render the dashboard.

The backend follows a layered architecture  
(app → domain → infrastructure → presentation)  
to ensure maintainability and scalability.

## Backend Structure Overview
```text
backend/
├─ data/                 # Input CSV file(s)
├─ artifacts/            # Generated JSON files and optional charts
│   └─ summaries/
│       └─ summary.json
└─ src/
    ├─ app/              # Entry point
    ├─ domain/           # Analysis logic
    ├─ infrastructure/   # File I/O utilities
    └─ presentation/     # (Optional) visualization / reporting
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
You can install all dependencies using
```bash
pip install -r requirements.txt
```

## How to Run
To execute the main analysis pipeline, run the following command.
```bash
python src/app/main.py
```

## Artifacts
All analysis results are stored in the following directory.
```text
artifacts/
  ├─ charts/      # Visualization images (plots, graphs)
  └─ summaries/   # Statistical summaries, CSV/Excel exports
```