[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Data Analysis Project
[KO](./docs/README.ko.md) | [EN](/README.md)

This project performs CSV-based data analysis using Python and visualizes the results through a dashboard built with Next.js (React).

The backend is responsible for loading CSV data, preprocessing, computing statistical metrics, and generating structured JSON artifacts.  
These artifacts are saved in the `artifacts/` directory for direct use by the frontend.

The frontend loads the generated JSON files and renders a visual dashboard consisting of charts and tables.

## Dataset Source
This project uses the following dataset sourced from Kaggle. 600+ programming questions with difficulty, description, examples, constraints, and test cases.

[**Coding Questions Dataset**](https://www.kaggle.com/datasets/guitaristboy/coding-questions-dataset)

License: MIT License  
Original dataset author: Kartikeya Pandey
> The original CSV dataset is included in this repository and is used as input for the Python analysis pipeline.  
> Redistribution and modification are permitted under the MIT License, and the dataset is processed to generate derived artifacts such as JSON files, charts, and Excel exports.

## Repositories
[frontend](/front) | [backend](/back)

## Project Structure

```text
final-project-data-analysis/
│
├─ back/                  # Python data analysis pipeline
│   ├─ README.md          # Backend-specific documentation
│   ├─ requirements.txt   # Python dependencies
│   ├─ data/              # Input CSV files
│   ├─ artifacts/         # Analysis outputs (JSON, charts, Excel exports)
│   └─ src/               # Source code (app/domain/infrastructure/presentation)
│
├─ front/                 # Next.js dashboard
│   ├─ README.md          # Frontend-specific documentation
│   ├─ package.json
│   ├─ public/            # Static assets
│   └─ src/               # Feature-sliced React code + shared generated data
│
├─ docs/                  # Documentation set (KO/EN)
│   ├─ README.ko.md              # Korean overview
│   ├─ requirements-analysis/    # 요구사항 및 목표 분석
│   ├─ io-design/                # 입출력/데이터 계약 정리
│   └─ system-architecture/      # 시스템 & 계층 구조 설명
│
└─ video/                 # Demonstration video
    └─ demo.mp4
```

## Backend Summary (back/)

- Entry: `back/src/app/main.py`
- Default dataset: `back/data/coding-questions-dataset/questions_dataset.csv`
- Outputs: `back/artifacts/json` (frontend-ready JSON), `back/artifacts/charts`, `back/artifacts/xlsx` (Excel splits), and `front/src/shared/data` (synced JSON
  for the UI).
- Run locally (from `back`):
  ```bash
  export PYTHONPATH="$(pwd)/src"
  python -m backend.app.main --data-file data/coding-questions-dataset/questions_dataset.csv
  ```

  ## Frontend Summary (front/)
- Next.js (App Router) dashboard with tabs for Overview, Difficulty, Tags, Structure, and Raw data.
- Uses generated JSON files in `front/src/shared/data` (e.g., `overview.json`, `difficulty.json`, `summary-full.json`).
- Start dev server (from `front`):
  ```bash
  npm install
  npm run dev
  # visit http://localhost:3000
  ```

## License
This project is licensed under the **MIT License**.
See the LICENSE file for the full text.