from pathlib import Path
from app.domain.normalize_excel_script import NormalizeExcelScript
import sys


def main():
    input_path: Path = Path(
        "/home/jvelasco/Desktop/mami/data/foropenal.detained-people-202602061640-(2).xlsx"
    )
    if not input_path.exists:
        raise FileNotFoundError

    output_path: Path = Path("Hello.xlsx")
    if output_path.exists():
        resonse: int = int(
            input(f"Archivo f{output_path} ya Existe. Desea sobreescribir?")
        )
        match resonse:
            case 1:
                NormalizeExcelScript(input_path, output_path).run_script()
            case 2:
                sys.exit()
            case _:
                NormalizeExcelScript(input_path, output_path).run_script()


if __name__ == "__main__":
    main()
