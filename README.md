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

## Main features

- Load Excel files from a desktop file picker
- Apply reusable data normalization rules
- Clean inconsistent text values
- Parse date columns
- Rename columns based on business rules
- Export normalized data to `.xlsx`
- Keep ETL logic separated from UI and file access layers

## How it works

1. The user selects an Excel file through the desktop interface.
2. The application loads the file into a Pandas DataFrame.
3. The normalization use case applies the transformation logic.
4. The normalized data is exported as a new Excel file.

## Architecture

The project follows a simple layered structure:

- `presentation`: desktop UI and file selection logic.
- `application`: use case orchestration.
- `domain`: data cleaning and normalization rules.
- `infrastructure`: Excel input/output operations.

This separation keeps the transformation logic independent from the user interface and file system details.

## Run locally

Clone the repository:

```bash
git clone https://github.com/jvelasco93/python-excel-etl-normalizer.git
cd python-excel-etl-normalizer
```

Install dependencies:

```bash
pip install -e .
```

Run the application:

```bash
python main.py
```

## Example workflow

1. Open the application.
2. Select an `.xlsx` input file.
3. Choose the output file path.
4. The application generates a normalized Excel file.

## Notes

This repository does not include real input files or sensitive data.

Sample files are intentionally excluded for privacy reasons. Future versions may include anonymized sample files to demonstrate the expected input and output format.

## Status

Work in progress.

Planned improvements:

- Add anonymized sample input/output files
- Add automated tests for transformation rules
- Improve error handling
- Add packaging instructions
- Add executable build instructions with PyInstaller

## Author

Julio Cesar Velasco  
Backend Developer focused on .NET, Python, SQL and data-driven backend solutions.

- GitHub: [@jvelasco93](https://github.com/jvelasco93)
