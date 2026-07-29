from PyQt6.QtWidgets import QApplication
from app.application.normalize_excel_use_case import NormalizeExcelUseCase
from app.presentation.qt_ui import FileSelection, run_ui, show_error, show_success


def main() -> None:
    app = QApplication.instance() or QApplication([])

    selection: FileSelection | None = run_ui()

    if selection is None:
        return

    try:
        NormalizeExcelUseCase().execute(selection.input_path, selection.output_path)
        show_success(
            f"Archivo normalizado exitosamente en la ruta:\n{str(selection.output_path)}"
        )
    except FileNotFoundError as error:
        show_error(
            title="Archivo no encontrado",
            message=(
                "No se pudo encontrar uno de los archivos seleccionados.\n\n"
                f"Detalle técnico: {error}"
            ),
        )
    except Exception as error:
        show_error(
            title="Error al procesar archivo",
            message=(
                "Ocurrió un error inesperado durante el procesamiento.\n\n"
                f"Detalle técnico: {error}"
            ),
        )

    app.processEvents()


if __name__ == "__main__":
    main()


# pyinstaller --onefile --noconsole --name Normalizador main.py