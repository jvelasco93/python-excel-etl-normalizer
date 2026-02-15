import pandas as pd
from pathlib import Path


def load_excel(excel_path: Path) -> pd.DataFrame:
    result: pd.DataFrame = (
        pd.read_excel(excel_path, engine="calamine", dtype=object)
        .fillna("")
        .astype(str)
    )
    result.insert(0, "#", range(1, len(result) + 1))
    return result


def export_excel(df: pd.DataFrame, output_path: Path) -> None:
    with pd.ExcelWriter(
        str(output_path), engine="xlsxwriter", datetime_format="dd/mm/yyyy"
    ) as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
