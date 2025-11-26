# Project Name?
주제 고민중

## Language
[EN](README.md) |  [KO](docs/README.ko.md)

---

## Project Overview
This project is a structured Python-based data analysis system. It is designed to load data from CSV or Excel files, perform preprocessing, conduct analytical operations, and generate visualizations. All generated outputs (charts, summaries, Excel exports) are stored in the `artifacts/` directory.

## Project Structure
```text
final-project-data-analysis/
│
├─ README.md # Main English documentation
├─ requirements.txt # Python dependencies
├─ .gitignore
│
├─ data/ # Input data (CSV, Excel, raw files)
│ └─ ...logs.csv
│
├─ artifacts/ # Generated analysis outputs (charts, summary files, exports)
│ ├─ charts/
│ └─ summaries/
│
├─ docs/ # Supplementary documentation (Korean docs included)
│ ├─ README.ko.md # Korean version of main documentation
│ ├─ requirements-analysis.md # Requirements analysis document
│ ├─ io-design.md # Input/Output (screen) design
│ └─ system-architecture.md # Description of the layered architecture
│
├─ video/ # Demo video for project presentation
│ └─ demo.mp4
│
└─ src/ # Source code (layered architecture)
├─ app/ # Application layer (entry point & pipeline)
│ ├─ main.py
│ └─ config.py
│
├─ domain/ # Domain layer (entities & business logic)
│ ├─ entities/
│ │ └─ ...log.py
│ └─ services/
│ └─ metrics.py
│
├─ infrastructure/ # Infrastructure layer (IO, logging, adapters)
│ ├─ io/
│ │ ├─ csv_loader.py
│ │ └─ artifact_writer.py
│ └─ logging/
│ └─ logger.py
│
└─ presentation/ # Presentation layer (visualization/report generation)
├─ charts/
│ ├─ stage_chart.py
│ └─ daily_chart.py
└─ reports/
└─ console_report.py
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