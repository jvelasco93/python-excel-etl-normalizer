# Normalizador ETL de Excel en Python

Herramienta ETL de escritorio construida con Python, Pandas y PyQt6 para limpiar, normalizar y exportar conjuntos de datos en Excel.

## Descripción general

El proyecto procesa archivos de Excel y aplica un conjunto de reglas de limpieza y normalización de datos definidas por el negocio, entre las que se incluyen:

- Parseo de columnas de fecha.
- Normalización de valores de género.
- Limpieza, capitalización y combinación de nacionalidades.
- Derivación de la edad a partir de la fecha de nacimiento.
- Renombrado de columnas según reglas de negocio.
- Limpieza de valores numéricos incrustados en texto.
- Exportación a un archivo de Excel normalizado.

La herramienta incluye una interfaz de escritorio sencilla para seleccionar el archivo de Excel de entrada y elegir la ruta de salida. Toda la interfaz y los mensajes mostrados al usuario están en español.

## Reglas de normalización

El pipeline de transformación se ejecuta en cadena (`run_script` en `normalize_excel_script.py`) en el siguiente orden:

| # | Paso | Acción |
|---|------|--------|
| 1 | `_parse_types` | Convierte a `datetime` las columnas de fecha según el formato esperado por cada una. |
| 2 | `_normalize_gender` | Traduce `male`/`female` a `Masculino`/`Femenino`. Otros valores se conservan sin cambios. |
| 3 | `_clean_nationalities` | Elimina el texto entre paréntesis que acompaña a las nacionalidades. |
| 4 | `_capitalize_nationalities` | Aplica formato de título (`title()`) a las nacionalidades. |
| 5 | `_apply_nationality_exceptions` | Aplica correcciones puntuales de nacionalidades (ver excepciones abajo). |
| 6 | `_build_final_nationality` | Combina la segunda nacionalidad con la primera en un solo valor. |
| 7 | `_change_column_names` | Renombra columnas según reglas de negocio. |
| 8 | `_clean_detention_cause_values` | Limpia los valores incrustados (`#\d+`) y sufijos `(C)` de la causa de detención. |
| 9 | `_clean_discapacity_values` | Limpia los valores incrustados (`#\d+`) de la discapacidad. |
| 10 | `_calculate_age` | Calcula la columna `Edad` a partir de la fecha de nacimiento. |

### Formatos de fecha por columna

| Columna | Formato esperado |
|---------|------------------|
| Fecha de Arresto | `%d/%m/%Y %I:%M%p` |
| Fecha de Nacimiento | `%Y-%m-%d %H:%M:%S` |
| Fecha Inicial Estatus 1 a 4 | `%d/%m/%Y %I:%M%p` |

Los valores que no puedan parsearse con el formato indicado quedan como `NaT` (no se elimina la fila).

### Excepciones de nacionalidad

| Valor de origen | Valor normalizado |
|-----------------|-------------------|
| trinidad y tobago | Trinitense |
| portugees | Portugués |
| guyana | Guyanés |

### Combinación de nacionalidades

Cuando una fila tiene primera y segunda nacionalidad, se combinan en el formato:

```text
Segunda Nacionalidad / Nacionalidad
```

Si solo existe una de las dos, se conserva tal cual.

## Esquema de columnas

El archivo de entrada puede contener más columnas que las documentadas; las reglas solo se aplican a las columnas que existen en el archivo cargado.

| Columna de entrada | Transformación | Columna de salida |
|--------------------|----------------|-------------------|
| — (generada) | Se inserta una numeración de fila `1..N` | `#` |
| — (generada) | Se calcula a partir de «Fecha de Nacimiento» | `Edad` |
| Género | Traducción `male`/`female` | Género |
| Nationality | Limpieza, capitalización, excepciones y combinación | Nacionalidad |
| Segunda Nacionalidad | Limpieza, capitalización y excepciones | Segunda Nacionalidad |
| Contacto | — | Nombre |
| Fecha de Arresto | Parseo a `datetime` | Fecha de Arresto |
| Fecha de Nacimiento | Parseo a `datetime` | Fecha de Nacimiento |
| Fecha Inicial Estatus 1 a 4 | Parseo a `datetime` | Fecha Inicial Estatus 1 a 4 |
| Causa de la Detención: | Limpieza de `#\d+` y sufijos `(C)` | Causa de la Detención: |
| Indique la discapacidad | Limpieza de `#\d+` | Indique la discapacidad |

Detalles técnicos de la carga y exportación:

- **Carga**: se usa `python-calamine` como motor de lectura. Todos los valores se cargan como texto (`dtype=object` + `.astype(str)`); las celdas vacías quedan como string vacío.
- **Numeración**: la columna `#` se inserta al cargar el archivo y persiste en la salida.
- **Exportación**: se usa `xlsxwriter`. La hoja se nombra `Sheet1`, las fechas se escriben con formato `dd/mm/yyyy` y se omite el índice de fila del DataFrame.

## Stack tecnológico

- Python (≥ 3.11)
- Pandas
- PyQt6
- python-calamine
- XlsxWriter
- OpenPyXL
- PyInstaller (solo en el grupo de desarrollo, para empaquetar)

## Arquitectura

El proyecto sigue una arquitectura por capas:

```text
.
├── main.py
├── app
│   ├── application
│   │   └── normalize_excel_use_case.py   # Orquestación del caso de uso
│   ├── domain
│   │   └── normalize_excel_script.py     # Reglas de limpieza y normalización
│   ├── infrastructure
│   │   └── excel_data_source.py          # Lectura y exportación de archivos Excel
│   └── presentation
│       └── qt_ui.py                      # Interfaz de escritorio (PyQt6)
└── pyproject.toml
```

- `presentation`: interfaz de escritorio, selección de archivos y mensajes al usuario.
- `application`: orquestación del caso de uso de normalización.
- `domain`: reglas de limpieza y normalización de datos.
- `infrastructure`: operaciones de entrada/salida con Excel.

Esta separación mantiene la lógica de transformación independiente de la interfaz de usuario y de los detalles del sistema de archivos.

## Características principales

- Selección del archivo de entrada y ruta de salida mediante diálogos nativos.
- Pipeline reutilizable de reglas de normalización.
- Limpieza de textos inconsistentes (paréntesis, valores incrustados, sufijos).
- Parseo de columnas de fecha con formatos específicos por columna.
- Deriva la edad a partir de la fecha de nacimiento.
- Combina y normaliza nacionalidades.
- Renombra columnas según reglas de negocio.
- Exporta los datos normalizados a `.xlsx`.
- Manejo de errores con mensajes claros para el usuario (archivo no encontrado o error de procesamiento).
- Lógica ETL separada de la interfaz y del acceso a archivos.

## Requisitos

- Python ≥ 3.11 (el archivo `.python-version` fija la versión de desarrollo en 3.14).
- [uv](https://docs.astral.sh/uv/) como gestor de dependencias y entornos (opcional, se recomienda).

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/jvelasco93/python-excel-etl-normalizer.git
cd python-excel-etl-normalizer
```

Instala las dependencias:

```bash
uv sync
```

Alternativa con `pip`:

```bash
pip install -e .
```

## Ejecución

```bash
python main.py
```

Flujo de uso:

1. Se abre un diálogo para seleccionar el archivo de Excel de entrada (`*.xlsx`).
2. Se elige la ruta y el nombre del archivo de salida.
3. El caso de uso carga el archivo, aplica el pipeline de normalización y exporta el resultado.
4. Se muestra un mensaje de éxito con la ruta del archivo generado (o un mensaje de error si algo falla).

## Empaquetado como ejecutable

Para generar un ejecutable único sin consola de Windows, se usa PyInstaller con el comando comentado en `main.py`:

```bash
pyinstaller --onefile --noconsole --name Normalizador main.py
```

## Estado

La documentación de este repositorio no incluye datos reales ni información sensible.

Mejoras futuras planificadas:

- Agregar archivos de ejemplo anonimizados que demuestren el formato de entrada y salida esperado.
- Agregar tests automatizados para las reglas de transformación.

## Autor

Julio Cesar Velasco
Desarrollador Backend enfocado en .NET, Python, SQL y soluciones backend orientadas a datos.

- GitHub: [@jvelasco93](https://github.com/jvelasco93)