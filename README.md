# Python Excel ETL Normalizer

Desktop ETL tool built with Python, Pandas and PyQt6 to clean, normalize and export Excel datasets.

## Overview

This project processes Excel files and applies a set of data cleaning and normalization rules, including:

- Date parsing
- Gender value normalization
- Nationality cleaning and formatting
- Column renaming
- Data validation and transformation
- Export to a normalized Excel file

The tool includes a simple desktop interface for selecting the input Excel file and choosing the output file path.

## Tech stack

- Python
- Pandas
- PyQt6
- python-calamine
- XlsxWriter
- OpenPyXL

## Project structure

```text
.
├── main.py
├── app
│   ├── application
│   │   └── normalize_excel_use_case.py
│   ├── domain
│   │   └── normalize_excel_script.py
│   ├── infrastructure
│   │   └── excel_data_source.py
│   └── presentation
│       └── qt_ui.py
└── pyproject.toml
```
