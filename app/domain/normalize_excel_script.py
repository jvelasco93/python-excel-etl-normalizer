import pandas as pd
import re


class NormalizeExcelScript:
    def run_script(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        result = self._parse_types(result)
        result = self._normalize_gender(result)
        result = self._clean_nationalities(result)
        result = self._capitalize_nationalities(result)
        result = self._apply_nationality_exceptions(result)
        result = self._build_final_nationality(result)
        return result

    def _parse_types(self, df: pd.DataFrame) -> pd.DataFrame:
        result = df.copy()
        result["Fecha de Arresto"] = pd.to_datetime(
            result["Fecha de Arresto"],
            format="%d/%m/%Y %I:%M%p",
            errors="coerce",
        )
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

        result = df.copy()
        result["Género"] = result["Género"].apply(_translate_gender)
        return result

    def _clean_nationalities(self, df: pd.DataFrame) -> pd.DataFrame:
        def _clean_value(value: str) -> str | None:
            if not value:
                return None

            cleaned = re.sub(r"\s*\([^)]*\)", "", value).strip()

            return cleaned if cleaned else None

        result = df.copy()
        for column in ["Nationality", "Segunda Nacionalidad"]:
            result[column] = result[column].apply(_clean_value)

        return result

    def _apply_nationality_exceptions(self, df: pd.DataFrame) -> pd.DataFrame:
        NATIONALITY_EXCEPTIONS: dict[str, str] = {
            "trinidad y tobago": "Trinidad y Tobago",
            "portugees": "Portugues",
        }

        def _apply_exceptions(value: str | None) -> str | None:
            if not isinstance(value, str) or not value:
                return None
            return NATIONALITY_EXCEPTIONS.get(value.lower().strip(), value)

        result = df.copy()
        result["Segunda Nacionalidad"] = result["Segunda Nacionalidad"].apply(
            _apply_exceptions
        )
        return result

    def _capitalize_nationalities(self, df: pd.DataFrame) -> pd.DataFrame:
        def _capitalize(value: str | None) -> str | None:
            if not isinstance(value, str) or not value:
                return None
            return value.title()

        result = df.copy()
        for column in ["Nationality", "Segunda Nacionalidad"]:
            result[column] = result[column].apply(_capitalize)
        return result

    def _build_final_nationality(self, df: pd.DataFrame) -> pd.DataFrame:
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
        result["Nationality"] = result.apply(_combine, axis=1)  # type: ignore
        return result
