from pathlib import Path
import pandas as pd

from app.domain.normalize_excel_script import NormalizeExcelScript
from app.infrastructure.excel_data_source import load_excel, export_excel


class NormalizeExcelUseCase:
    @staticmethod
    def execute(input_path: Path, output_path: Path) -> None:
        source_df: pd.DataFrame = load_excel(input_path)
        normalized_df: pd.DataFrame = NormalizeExcelScript().run_script(source_df)
        export_excel(normalized_df, output_path)
