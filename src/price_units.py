from __future__ import annotations

import pandas as pd


def values_to_display(values, unit_config: dict):
    source_unit = unit_config.get("source_unit", "100k_usd")
    display_unit = unit_config.get("display_unit", "10k_rmb")
    usd_to_rmb = float(unit_config.get("usd_to_rmb", 6.6))

    if source_unit == "100k_usd" and display_unit == "10k_rmb":
        return pd.Series(values) * 10 * usd_to_rmb
    if source_unit == display_unit:
        return pd.Series(values)

    raise ValueError(f"Unsupported price unit conversion: {source_unit} -> {display_unit}")


def display_unit_label(unit_config: dict) -> str:
    display_unit = unit_config.get("display_unit", "10k_rmb")
    if display_unit == "10k_rmb":
        return "万元人民币 / 10k RMB"
    if display_unit == "100k_usd":
        return "十万美元 / 100k USD"
    return display_unit


def source_unit_label(unit_config: dict) -> str:
    source_unit = unit_config.get("source_unit", "100k_usd")
    if source_unit == "100k_usd":
        return "十万美元 / 100k USD"
    return source_unit
