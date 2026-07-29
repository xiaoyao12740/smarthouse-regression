from __future__ import annotations

import json
from pathlib import Path


def load_field_descriptions(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def display_name(column: str, descriptions: dict, language: str = "bilingual") -> str:
    item = descriptions.get(column, {})
    zh_name = item.get("zh_name", column)
    en_name = item.get("en_name", column)

    if language == "zh":
        return zh_name
    if language == "en":
        return en_name
    return f"{zh_name} / {en_name} ({column})"


def bilingual_column_name(column: str, descriptions: dict) -> str:
    item = descriptions.get(column, {})
    zh_name = item.get("zh_name")
    en_name = item.get("en_name")
    if zh_name and en_name:
        return f"{zh_name} / {en_name} ({column})"
    return column


def rename_columns_for_display(columns: list[str], descriptions: dict) -> dict:
    return {column: bilingual_column_name(column, descriptions) for column in columns}
