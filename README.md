[KO](./docs/README.ko.md) | [EN](/README.md)

# Data Analysis Project
This project performs CSV-based data analysis using Python and visualizes the results through a dashboard built with Next.js (React).

The backend is responsible for loading CSV data, preprocessing, computing statistical metrics, and generating structured JSON artifacts.  
These artifacts are saved in the `artifacts/` directory for direct use by the frontend.

The frontend loads the generated JSON files and renders a visual dashboard consisting of charts and tables.

## Dataset Source
This project uses the following dataset sourced from Kaggle:

**Coding Questions Dataset**  
https://www.kaggle.com/datasets/guitaristboy/coding-questions-dataset

The dataset contains 600+ programming questions with metadata such as
title, description, difficulty, examples, constraints, and test cases.

## Repositories
[frontend](/front) | [backend](/back)

## Project Structure
```text
final-project-data-analysis/
│
├─ backend/              # Python data analysis pipeline
│   ├─ README.md         # Backend-specific documentation
│   ├─ requirements.txt  # Python dependencies
│   ├─ data/             # Input data (CSV files)
│   ├─ artifacts/        # Analysis outputs (JSON, charts, summaries)
│   └─ src/              # Source code (app/domain/infrastructure/presentation)
│
├─ frontend/             # Next.js-based web dashboard
│   ├─ README.md         # Frontend-specific documentation
│   ├─ package.json
│   ├─ public/           # Static assets (e.g., summary.json)
│   └─ src/              # Next.js/React source code
│
├─ docs/                 # Documentation set
│   ├─ README.ko.md              # Korean version of main documentation
│   ├─ requirements-analysis.md  # Requirements analysis
│   ├─ io-design.md              # Input/Output and screen design
│   └─ system-architecture.md    # System & layered architecture description
│
└─ video/                # Demonstration video
    └─ demo.mp4
```

## License

This project is licensed under the **MIT License**.

You are free to use, copy, modify, merge, publish, distribute, sublicense,  
and/or sell copies of this software, provided that proper credit is given  
to the original author.

Unauthorized use without attribution, including academic misuse  
(e.g., using this work in reports, papers, or publications without citation)  
is strictly prohibited.

For full details, see the LICENSE file.