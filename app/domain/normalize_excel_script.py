import re
from typing import Callable, Iterable

import pandas as pd


class NormalizeExcelScript:
    def run_script(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        result = self._parse_types(result)
        result = self._normalize_gender(result)
        result = self._clean_nationalities(result)
        result = self._capitalize_nationalities(result)
        result = self._apply_nationality_exceptions(result)
        result = self._build_final_nationality(result)
        result = self._change_column_names(result)
        result = self._clean_detention_cause_values(result)
        result = self._clean_discapacity_values(result)
        return result

    def _apply_if_column_exists(
        self,
        df: pd.DataFrame,
        column_name: str,
        transform: Callable[[pd.Series], pd.Series],
    ) -> pd.DataFrame:
        if column_name not in df.columns:
            return df.copy()

        result = df.copy()
        result[column_name] = transform(result[column_name])
        return result

    def _apply_per_existing_columns(
        self,
        df: pd.DataFrame,
        column_names: Iterable[str],
        transform: Callable[[pd.Series], pd.Series],
    ) -> pd.DataFrame:
        existing_columns = [column for column in column_names if column in df.columns]
        if not existing_columns:
            return df.copy()

        result = df.copy()
        for column in existing_columns:
            result[column] = transform(result[column])
        return result

    def _clean_discapacity_values(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._apply_if_column_exists(
            df,
            "Indique la discapacidad",
            lambda series: series.astype(str)
            .str.replace(r"^#\d+\s*", "", regex=True)
            .str.strip(),
        )

    def _clean_detention_cause_values(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._apply_if_column_exists(
            df,
            "Causa de la Detención:",
            lambda series: series.astype(str)
            .str.replace(r"^#\d+\s*", "", regex=True)
            .str.replace(r"\s*\(C\)$", "", regex=True)
            .str.strip(),
        )

    def _change_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        # Cambiar los nombres de las columnas siguientes:
        # Nationality -> Nacionalidad
        # Contacto -> Nombre
        column_mapping = {
            "Nationality": "Nacionalidad",
            "Contacto": "Nombre",
        }
        result = df.copy()
        result.rename(columns=column_mapping, inplace=True)
        return result

    def _parse_types(self, df: pd.DataFrame) -> pd.DataFrame:
        def _parse_datetime(
            df_: pd.DataFrame, column_name: str, fmt: str
        ) -> pd.DataFrame:
            if column_name in df_.columns:
                df_[column_name] = pd.to_datetime(
                    df_[column_name], format=fmt, errors="coerce"
                )

        formats = {
            "Fecha de Arresto": "%d/%m/%Y %I:%M%p",
            "Fecha de Nacimiento": "%Y-%m-%d %H:%M:%S",
            "Fecha Inicial Estatus 1": "%d/%m/%Y %I:%M%p",
            "Fecha Inicial Estatus 2": "%d/%m/%Y %I:%M%p",
            "Fecha Inicial Estatus 3": "%d/%m/%Y %I:%M%p",
            "Fecha Inicial Estatus 4": "%d/%m/%Y %I:%M%p",

        }
        result = df.copy()
        for column_name, fmt in formats.items():
            _parse_datetime(result, column_name, fmt)
        return result

    def _normalize_gender(self, df: pd.DataFrame) -> pd.DataFrame:
        def _translate_gender(a_value: str) -> str | None:
            GENDER_TRANSLATIONS = {
                "male": "Masculino",
                "female": "Femenino",
            }

            if not a_value:
                return a_value

            return GENDER_TRANSLATIONS.get(a_value.lower(), a_value)

        return self._apply_if_column_exists(
            df,
            "Género",
            lambda series: series.apply(_translate_gender),
        )

    def _clean_nationalities(self, df: pd.DataFrame) -> pd.DataFrame:
        def _clean_value(value: str) -> str | None:
            if not value:
                return None

            cleaned = re.sub(r"\s*\([^)]*\)", "", value).strip()

            return cleaned if cleaned else None

        return self._apply_per_existing_columns(
            df,
            ["Nationality", "Segunda Nacionalidad"],
            lambda series: series.apply(_clean_value),
        )

    def _apply_nationality_exceptions(self, df: pd.DataFrame) -> pd.DataFrame:
        NATIONALITY_EXCEPTIONS: dict[str, str] = {
            "trinidad y tobago": "Trinitense",
            "portugees": "Portugués",
            "guyana": "Guyanés",
        }

        def _apply_exceptions(value: str | None) -> str | None:
            if not isinstance(value, str) or not value:
                return None
            return NATIONALITY_EXCEPTIONS.get(value.lower().strip(), value)

        return self._apply_per_existing_columns(
            df,
            ["Segunda Nacionalidad", "Nationality"],
            lambda series: series.apply(_apply_exceptions),
        )

    def _capitalize_nationalities(self, df: pd.DataFrame) -> pd.DataFrame:
        def _capitalize(value: str | None) -> str | None:
            if not isinstance(value, str) or not value:
                return None
            return value.title()

        return self._apply_per_existing_columns(
            df,
            ["Nationality", "Segunda Nacionalidad"],
            lambda series: series.apply(_capitalize),
        )

    def _build_final_nationality(self, df: pd.DataFrame) -> pd.DataFrame:
        if "Nationality" not in df.columns and "Segunda Nacionalidad" not in df.columns:
            return df.copy()

        def _combine(row: pd.Series) -> str | None:
            nat1 = row.get("Nationality")
            nat2 = row.get("Segunda Nacionalidad")

            has_nat1 = isinstance(nat1, str) and nat1
            has_nat2 = isinstance(nat2, str) and nat2

            if has_nat1 and has_nat2:
                return f"{nat2} / {nat1}"

            if has_nat1:
                return nat1

            if has_nat2:
                return nat2

            return None

        result = df.copy()
        if "Nationality" not in result.columns:
            result["Nationality"] = None
        if "Segunda Nacionalidad" not in result.columns:
            result["Segunda Nacionalidad"] = None

        result["Nationality"] = result.apply(_combine, axis=1)  # type: ignore
        return result
