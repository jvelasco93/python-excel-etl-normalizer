from pathlib import Path
from typing import NamedTuple

from PyQt6.QtWidgets import QFileDialog, QMessageBox


class FileSelection(NamedTuple):
    input_path: Path
    output_path: Path


def show_success(message: str) -> None:
    QMessageBox.information(None, "Éxito", message)


def show_error(title: str, message: str) -> None:
    QMessageBox.critical(None, title, message)


def _get_suggested_output_file_name(input_file_path: Path) -> str:
    return f"{input_file_path.stem}-normalized.xlsx"


def _downloads_folder() -> str:
    return str(Path.home() / "Downloads")


def _input_file_path() -> Path | None:
    selected_file, _ = QFileDialog.getOpenFileName(
        parent=None,
        caption="Selecciona el archivo de Excel a procesar",
        directory=_downloads_folder(),
        filter="Archivos Excel (*.xlsx)",
    )
    if not selected_file:
        return None
    return Path(selected_file)


def _output_file_path(suggested_file_name: str, base_directory: Path) -> Path | None:
    selected_file, _ = QFileDialog.getSaveFileName(
        parent=None,
        caption="Selecciona el archivo de Excel de salida",
        directory=str(base_directory / suggested_file_name),
        filter="Archivos Excel (*.xlsx)",
    )
    if not selected_file:
        return None
    return Path(selected_file)


def run_ui() -> FileSelection | None:
    input_path = _input_file_path()
    if input_path is None:
        return None

    output_path = _output_file_path(
        suggested_file_name=_get_suggested_output_file_name(input_path),
        base_directory=input_path.parent,
    )
    if output_path is None:
        return None

    return FileSelection(input_path=input_path, output_path=output_path)
