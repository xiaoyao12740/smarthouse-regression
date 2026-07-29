from __future__ import annotations

import json
import math
import sys
from io import BytesIO
from pathlib import Path
import html

import altair as alt
import joblib
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from field_metadata import display_name, load_field_descriptions
from price_units import display_unit_label, source_unit_label, values_to_display

ZH = {
    "title": "\u667a\u80fd\u623f\u4ef7\u9884\u6d4b",
    "caption": (
        "\u57fa\u4e8e California Housing \u6570\u636e\u96c6\u7684\u56de\u5f52\u9884\u6d4b\u6f14\u793a\u3002"
        "\u6a21\u578b\u6536\u5165\u5b57\u6bb5\u4f7f\u7528\u4e07\u7f8e\u5143/\u5e74\uff0c"
        "\u623f\u4ef7\u539f\u59cb\u8f93\u51fa\u4f7f\u7528\u5341\u4e07\u7f8e\u5143\u3002"
    ),
    "rate_note": "\u4eba\u6c11\u5e01\u7ed3\u679c\u6309\u56fa\u5b9a\u5047\u8bbe 1 USD = {rate} RMB \u6362\u7b97\uff0c\u4ec5\u7528\u4e8e\u4f5c\u54c1\u5c55\u793a\u3002",
    "missing_model": "\u672a\u627e\u5230\u5df2\u8bad\u7ec3\u6a21\u578b\u3002\u8bf7\u5148\u8fd0\u884c\u8bad\u7ec3\u811a\u672c\u751f\u6210 models/house_price_model.joblib\u3002",
    "predict_tab": "\u623f\u4ef7\u9884\u6d4b / Prediction",
    "model_tab": "\u6a21\u578b\u4fe1\u606f / Model",
    "fields_tab": "\u5b57\u6bb5\u8bf4\u660e / Fields",
    "input_title": "\u8f93\u5165\u623f\u5c4b\u533a\u57df\u7279\u5f81 / Enter House Area Features",
    "unit_info": (
        "\u5355\u4f4d\u6362\u7b97\u8bf4\u660e\uff1a\u9875\u9762\u5141\u8bb8\u7528\u66f4\u81ea\u7136\u7684\u6536\u5165\u5355\u4f4d\u8f93\u5165\uff0c"
        "\u7a0b\u5e8f\u4f1a\u81ea\u52a8\u6362\u7b97\u6210\u6a21\u578b\u9700\u8981\u7684 MedInc\uff0c\u4e5f\u5c31\u662f\u201c\u4e07\u7f8e\u5143/\u5e74\u201d\u3002"
        "\u623f\u4ef7\u9884\u6d4b\u7ed3\u679c\u4f1a\u540c\u65f6\u663e\u793a\u539f\u59cb\u5355\u4f4d\u3001\u7f8e\u5143\u548c\u4eba\u6c11\u5e01\u4f30\u7b97\u3002"
    ),
    "income": "\u5c45\u6c11\u6536\u5165\u4e2d\u4f4d\u6570 / Median income",
    "income_help": "\u53ef\u4ee5\u9009\u62e9\u4e0d\u540c\u6536\u5165\u5355\u4f4d\u3002\u7a0b\u5e8f\u4f1a\u6362\u7b97\u4e3a\u6a21\u578b\u5b57\u6bb5 MedInc\uff0c\u5373\u4e07\u7f8e\u5143/\u5e74\u3002",
    "income_unit": "\u6536\u5165\u5355\u4f4d / Income unit",
    "raw_income_unit": "\u6a21\u578b\u539f\u59cb\u5355\u4f4d\uff1a\u4e07\u7f8e\u5143/\u5e74",
    "usd_year": "\u7f8e\u5143/\u5e74",
    "usd_month": "\u7f8e\u5143/\u6708",
    "rmb_year": "\u4eba\u6c11\u5e01/\u5e74",
    "rmb_month": "\u4eba\u6c11\u5e01/\u6708",
    "converted_income": "\u6362\u7b97\u540e\u7684\u6a21\u578b\u8f93\u5165 MedInc = {value:.4f} \u4e07\u7f8e\u5143/\u5e74",
    "predict_button": "\u9884\u6d4b\u623f\u4ef7 / Predict Price",
    "raw_prediction": "\u539f\u59cb\u9884\u6d4b / Raw",
    "usd_estimate": "\u7f8e\u5143\u4f30\u7b97 / USD",
    "rmb_estimate": "\u4eba\u6c11\u5e01\u4f30\u7b97 / RMB",
    "rate_statement": (
        "\u6c47\u7387\u58f0\u660e\uff1a\u4eba\u6c11\u5e01\u5c55\u793a\u6309\u56fa\u5b9a\u5047\u8bbe 1 USD = {rate} RMB \u6362\u7b97\uff0c"
        "\u7528\u4e8e\u9879\u76ee\u5c55\u793a\u548c\u76f4\u89c2\u7406\u89e3\uff0c\u4e0d\u4ee3\u8868\u5b9e\u65f6\u6c47\u7387\u6216\u771f\u5b9e\u4e2d\u56fd\u623f\u4ef7\u6570\u636e\u3002"
    ),
    "raw_output": "\u9884\u6d4b\u623f\u4ef7\u539f\u59cb\u503c / Raw prediction (100k USD)",
    "display_output": "\u9884\u6d4b\u623f\u4ef7 / Predicted price ({unit})",
    "download_csv": "\u4e0b\u8f7d\u9884\u6d4b\u8868\u683c / Download CSV",
    "download_png": "\u4e0b\u8f7d\u9884\u6d4b\u56fe\u7247 / Download PNG",
    "drivers": "\u4e3b\u8981\u5f71\u54cd\u56e0\u7d20 / Key Drivers",
    "driver_caption": "\u8fd9\u91cc\u4f7f\u7528\u968f\u673a\u68ee\u6797\u7684 feature_importances_\uff0c\u7528\u4e8e\u63d0\u4f9b\u4e00\u4e2a\u8f7b\u91cf\u7ea7\u6a21\u578b\u89e3\u91ca\u3002",
    "model_perf": "\u6a21\u578b\u8868\u73b0 / Model Performance",
    "current_model": "\u5f53\u524d\u6a21\u578b / Model",
    "model_size": "\u6a21\u578b\u6587\u4ef6\u5927\u5c0f / Model file size: {size:.2f} MB",
    "field_dict": "\u5b57\u6bb5\u8bcd\u5178 / Field Dictionary",
}


def load_config() -> dict:
    return json.loads((PROJECT_ROOT / "config.json").read_text(encoding="utf-8"))


@st.cache_resource
def load_model(model_path: str):
    return joblib.load(PROJECT_ROOT / model_path)


@st.cache_data
def load_metrics(metrics_path: str) -> dict:
    path = PROJECT_ROOT / metrics_path
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


@st.cache_data
def load_comparison(comparison_path: str) -> pd.DataFrame:
    path = PROJECT_ROOT / comparison_path
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def format_model_name(name: str) -> str:
    names = {
        "random_forest": "\u968f\u673a\u68ee\u6797 / Random Forest",
        "ridge": "\u5cad\u56de\u5f52 / Ridge Regression",
        "linear_regression": "\u7ebf\u6027\u56de\u5f52 / Linear Regression",
    }
    return names.get(name, name)


def convert_income_to_model_unit(amount: float, unit: str, exchange_rate: float) -> float:
    if unit == ZH["raw_income_unit"]:
        return amount
    if unit == ZH["usd_year"]:
        return amount / 10000
    if unit == ZH["usd_month"]:
        return amount * 12 / 10000
    if unit == ZH["rmb_year"]:
        return amount / exchange_rate / 10000
    if unit == ZH["rmb_month"]:
        return amount * 12 / exchange_rate / 10000
    raise ValueError(f"Unsupported income unit: {unit}")


def feature_importance_table(bundle: dict, field_descriptions: dict) -> pd.DataFrame:
    pipeline = bundle["pipeline"]
    model = pipeline.named_steps["model"]
    feature_columns = bundle["feature_columns"]
    if not hasattr(model, "feature_importances_"):
        return pd.DataFrame()

    rows = []
    for feature, importance in zip(feature_columns, model.feature_importances_):
        rows.append(
            {
                "feature": display_name(feature, field_descriptions, "bilingual"),
                "importance": float(importance),
            }
        )
    data = pd.DataFrame(rows).sort_values("importance", ascending=False)
    total = float(data["importance"].sum()) or 1.0
    data["share"] = data["importance"] / total
    return data


def render_feature_importance(importance: pd.DataFrame) -> None:
    if importance.empty:
        return

    max_value = float(importance["importance"].max()) or 1.0
    for _, row in importance.iterrows():
        label = str(row["feature"])
        value = float(row["importance"])
        share = float(row["share"])
        normalized = min(max(value / max_value, 0.0), 1.0)
        label_col, bar_col, value_col, share_col = st.columns([3, 5, 1, 1])
        label_col.write(label)
        bar_col.progress(normalized)
        value_col.write(f"{value:.4f}")
        share_col.write(f"{share:.1%}")


def render_importance_charts(importance: pd.DataFrame) -> None:
    if importance.empty:
        return

    display = importance.copy()
    display["share_percent"] = display["share"] * 100
    display["rank"] = range(1, len(display) + 1)

    top3 = display.head(3)
    st.markdown(
        (
            f"**Top 3 / 主要前三项：** "
            f"{top3.iloc[0]['feature']} ({top3.iloc[0]['share']:.1%})，"
            f"{top3.iloc[1]['feature']} ({top3.iloc[1]['share']:.1%})，"
            f"{top3.iloc[2]['feature']} ({top3.iloc[2]['share']:.1%})。"
        )
    )

    chart_col, table_col = st.columns([2, 1])
    with chart_col:
        donut = (
            alt.Chart(display)
            .mark_arc(innerRadius=70, outerRadius=130)
            .encode(
                theta=alt.Theta("share:Q", title="Share"),
                color=alt.Color("feature:N", title="Feature"),
                tooltip=[
                    alt.Tooltip("feature:N", title="Feature"),
                    alt.Tooltip("importance:Q", title="Importance", format=".4f"),
                    alt.Tooltip("share_percent:Q", title="Share %", format=".1f"),
                ],
            )
            .properties(height=340, title="权重占比 / Importance Share")
        )
        st.altair_chart(donut, use_container_width=True)

    with table_col:
        table = display[["rank", "feature", "importance", "share_percent"]].rename(
            columns={
                "rank": "排名 / Rank",
                "feature": "因素 / Feature",
                "importance": "重要性 / Importance",
                "share_percent": "占比% / Share %",
            }
        )
        st.dataframe(
            table,
            use_container_width=True,
            hide_index=True,
            column_config={
                "重要性 / Importance": st.column_config.NumberColumn(format="%.4f"),
                "占比% / Share %": st.column_config.NumberColumn(format="%.1f"),
            },
        )


def build_prediction_image(
    raw_prediction: float,
    usd_prediction: float,
    rmb_prediction: float,
    exchange_rate: float,
    top_drivers: pd.DataFrame,
) -> bytes:
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis("off")
    ax.text(0.04, 0.92, "SmartHouse AI Predictor", fontsize=22, weight="bold")
    ax.text(0.04, 0.84, "Prediction Summary / 房价预测摘要", fontsize=15, weight="bold")
    ax.text(0.04, 0.74, f"Raw prediction: {raw_prediction:.3f} (100k USD)", fontsize=13)
    ax.text(0.04, 0.66, f"Estimated USD: ${usd_prediction:,.0f}", fontsize=13)
    ax.text(0.04, 0.58, f"Estimated RMB: {rmb_prediction:,.1f} x 10k RMB", fontsize=13)
    ax.text(0.04, 0.50, f"Exchange-rate assumption: 1 USD = {exchange_rate} RMB", fontsize=11)
    ax.text(0.04, 0.45, "For portfolio demonstration only. Not real-time FX or real Chinese housing data.", fontsize=10)

    if not top_drivers.empty:
        ax.text(0.04, 0.34, "Top Drivers / Main factors", fontsize=14, weight="bold")
        y = 0.27
        for _, row in top_drivers.head(3).iterrows():
            label = str(row["feature"])
            share = float(row["share"])
            ax.text(0.06, y, f"- {label}: {share:.1%}", fontsize=11)
            y -= 0.07

    buffer = BytesIO()
    fig.tight_layout()
    fig.savefig(buffer, format="png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()


def svg_escape(value: str) -> str:
    return html.escape(str(value), quote=True)


def wrap_label(value: str, limit: int = 34) -> list[str]:
    text = str(value)
    if len(text) <= limit:
        return [text]
    parts = text.split(" / ")
    if len(parts) >= 2:
        first = parts[0]
        rest = " / ".join(parts[1:])
        return [first, rest]
    return [text[:limit], text[limit:]]


def svg_text(x: float, y: float, lines: list[str], size: int = 16, weight: str = "500") -> str:
    tspans = []
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else size * 1.25
        tspans.append(f'<tspan x="{x}" dy="{dy}">{svg_escape(line)}</tspan>')
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
        'font-family="Microsoft YaHei, SimHei, Arial, sans-serif">'
        + "".join(tspans)
        + "</text>"
    )


def build_prediction_svg(
    raw_prediction: float,
    usd_prediction: float,
    rmb_prediction: float,
    exchange_rate: float,
    top_drivers: pd.DataFrame,
) -> bytes:
    driver_lines = []
    for _, row in top_drivers.head(3).iterrows():
        driver_lines.append(f"{row['feature']} ({float(row['share']):.1%})")

    driver_text = "".join(
        svg_text(70, 390 + index * 34, [f"{index + 1}. {line}"], size=15)
        for index, line in enumerate(driver_lines)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="560" viewBox="0 0 1100 560">
  {svg_text(70, 70, ["SmartHouse AI Predictor", "房价预测摘要 / Prediction Summary"], size=28, weight="700")}
  {svg_text(70, 175, [f"原始预测 / Raw prediction: {raw_prediction:.3f} (100k USD)"], size=20)}
  {svg_text(70, 225, [f"美元估算 / Estimated USD: ${usd_prediction:,.0f}"], size=20)}
  {svg_text(70, 275, [f"人民币估算 / Estimated RMB: {rmb_prediction:,.1f} 万元"], size=20)}
  {svg_text(70, 325, [f"汇率假设 / Exchange-rate assumption: 1 USD = {exchange_rate} RMB"], size=16)}
  {svg_text(70, 365, ["Top 3 / 主要影响因素"], size=20, weight="700")}
  {driver_text}
  {svg_text(70, 520, ["仅用于作品展示，不代表实时汇率或真实中国房价数据。"], size=14)}
</svg>"""
    return svg.encode("utf-8")


def build_importance_bar_image(importance: pd.DataFrame) -> bytes:
    display = importance.sort_values("importance", ascending=True)
    fig_height = max(4.8, len(display) * 0.58)
    fig, ax = plt.subplots(figsize=(11, fig_height))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    labels = display["feature"].astype(str).tolist()
    values = display["importance"].astype(float).tolist()
    shares = display["share"].astype(float).tolist()
    ax.barh(labels, values, color="#2d8fe3")
    for index, (value, share) in enumerate(zip(values, shares)):
        ax.text(value + max(values) * 0.015, index, f"{value:.4f}  {share:.1%}", va="center", fontsize=10)

    ax.set_xlabel("Importance")
    ax.set_title("Key Drivers / Feature Importance", fontsize=16, weight="bold")
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.grid(axis="x", alpha=0.18)
    ax.tick_params(axis="y", labelsize=10)
    fig.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=200, transparent=True, bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()


def build_importance_bar_svg(importance: pd.DataFrame) -> bytes:
    width = 1400
    row_height = 82
    top = 110
    left = 420
    bar_width = 730
    height = top + len(importance) * row_height + 80
    max_value = float(importance["importance"].max()) or 1.0
    rows = []
    for index, (_, row) in enumerate(importance.iterrows()):
        y = top + index * row_height
        label_lines = wrap_label(str(row["feature"]), 28)
        value = float(row["importance"])
        share = float(row["share"])
        fill_width = max(value / max_value * bar_width, 4)
        rows.append(svg_text(40, y + 12, label_lines, size=17))
        rows.append(f'<rect x="{left}" y="{y - 14}" width="{bar_width}" height="18" rx="5" fill="#d8dee9" opacity="0.55"/>')
        rows.append(f'<rect x="{left}" y="{y - 14}" width="{fill_width:.2f}" height="18" rx="5" fill="#2d8fe3"/>')
        rows.append(svg_text(left + bar_width + 35, y + 3, [f"{value:.4f}", f"{share:.1%}"], size=16, weight="700"))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  {svg_text(40, 52, ["主要影响因素 / Key Drivers", "Feature Importance"], size=28, weight="700")}
  {"".join(rows)}
</svg>"""
    return svg.encode("utf-8")


def build_importance_donut_image(importance: pd.DataFrame) -> bytes:
    labels = importance["feature"].astype(str).tolist()
    shares = importance["share"].astype(float).tolist()
    legend_labels = [f"{label} ({share:.1%})" for label, share in zip(labels, shares)]

    fig, ax = plt.subplots(figsize=(9, 6))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")
    wedges, _ = ax.pie(
        shares,
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.42, "edgecolor": "white", "linewidth": 1},
    )
    ax.set_title("Importance Share / 权重占比", fontsize=16, weight="bold")
    ax.legend(
        wedges,
        legend_labels,
        title="Feature",
        loc="center left",
        bbox_to_anchor=(1.0, 0.5),
        frameon=False,
        fontsize=9,
    )
    ax.set_aspect("equal")
    fig.tight_layout()

    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=200, transparent=True, bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return buffer.getvalue()


def donut_path(cx: float, cy: float, outer_r: float, inner_r: float, start: float, end: float) -> str:
    large_arc = 1 if end - start > math.pi else 0
    x1 = cx + outer_r * math.cos(start)
    y1 = cy + outer_r * math.sin(start)
    x2 = cx + outer_r * math.cos(end)
    y2 = cy + outer_r * math.sin(end)
    x3 = cx + inner_r * math.cos(end)
    y3 = cy + inner_r * math.sin(end)
    x4 = cx + inner_r * math.cos(start)
    y4 = cy + inner_r * math.sin(start)
    return (
        f"M {x1:.2f} {y1:.2f} "
        f"A {outer_r} {outer_r} 0 {large_arc} 1 {x2:.2f} {y2:.2f} "
        f"L {x3:.2f} {y3:.2f} "
        f"A {inner_r} {inner_r} 0 {large_arc} 0 {x4:.2f} {y4:.2f} Z"
    )


def build_importance_donut_svg(importance: pd.DataFrame) -> bytes:
    colors = ["#1672c9", "#ff8a00", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f"]
    cx, cy = 330, 360
    outer_r, inner_r = 230, 135
    start = -math.pi / 2
    paths = []
    legend = []
    for index, (_, row) in enumerate(importance.iterrows()):
        share = float(row["share"])
        end = start + share * math.tau
        color = colors[index % len(colors)]
        paths.append(f'<path d="{donut_path(cx, cy, outer_r, inner_r, start, end)}" fill="{color}" stroke="white" stroke-width="2"/>')
        legend_y = 175 + index * 54
        label = f"{row['feature']} ({share:.1%})"
        legend.append(f'<rect x="690" y="{legend_y - 16}" width="24" height="16" fill="{color}"/>')
        legend.append(svg_text(728, legend_y, wrap_label(label, 44), size=16))
        start = end

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="760" viewBox="0 0 1280 760">
  {svg_text(70, 70, ["权重占比 / Importance Share"], size=30, weight="700")}
  {"".join(paths)}
  {svg_text(690, 120, ["Feature"], size=18, weight="700")}
  {"".join(legend)}
</svg>"""
    return svg.encode("utf-8")


def main() -> None:
    st.set_page_config(page_title="SmartHouse AI Predictor", page_icon="House", layout="wide")

    config = load_config()
    data_config = config["data"]
    output_config = config["outputs"]
    presentation_config = config.get("presentation", {})
    unit_config = presentation_config.get("price_unit", {})
    field_descriptions = load_field_descriptions(PROJECT_ROOT / presentation_config.get("field_descriptions_path", ""))
    exchange_rate = float(unit_config.get("usd_to_rmb", 6.6))

    st.title(f"SmartHouse AI Predictor / {ZH['title']}")
    st.caption(ZH["caption"] + ZH["rate_note"].format(rate=exchange_rate))

    model_path = PROJECT_ROOT / output_config["model_path"]
    if not model_path.exists():
        st.error(ZH["missing_model"])
        return

    bundle = load_model(output_config["model_path"])
    feature_columns = bundle["feature_columns"]
    pipeline = bundle["pipeline"]
    metrics = load_metrics(output_config["metrics_path"])
    comparison = load_comparison(output_config["model_comparison_path"])
    importance = feature_importance_table(bundle, field_descriptions)

    tab_predict, tab_model, tab_fields = st.tabs([ZH["predict_tab"], ZH["model_tab"], ZH["fields_tab"]])

    with tab_predict:
        st.subheader(ZH["input_title"])
        st.info(ZH["unit_info"])

        defaults = {
            "HouseAge": 25.0,
            "AveRooms": 5.5,
            "AveBedrms": 1.1,
            "Population": 1200.0,
            "AveOccup": 2.8,
            "Latitude": 34.0,
            "Longitude": -118.0,
        }

        values = {}
        income_col, unit_col = st.columns([2, 1])
        with income_col:
            income_amount = st.number_input(
                ZH["income"],
                value=5.0,
                min_value=0.0,
                help=ZH["income_help"],
            )
        with unit_col:
            income_unit = st.selectbox(
                ZH["income_unit"],
                [ZH["raw_income_unit"], ZH["usd_year"], ZH["usd_month"], ZH["rmb_year"], ZH["rmb_month"]],
            )
        values["MedInc"] = convert_income_to_model_unit(income_amount, income_unit, exchange_rate)
        st.caption(ZH["converted_income"].format(value=values["MedInc"]))

        columns = st.columns(2)
        unit_hints = {
            "HouseAge": "\u5355\u4f4d\uff1a\u5e74 / years",
            "AveRooms": "\u5355\u4f4d\uff1a\u95f4/\u6237 / rooms per household",
            "AveBedrms": "\u5355\u4f4d\uff1a\u95f4/\u6237 / bedrooms per household",
            "Population": "\u5355\u4f4d\uff1a\u4eba / people",
            "AveOccup": "\u5355\u4f4d\uff1a\u4eba/\u6237 / people per household",
            "Latitude": "\u5355\u4f4d\uff1a\u5ea6 / degrees",
            "Longitude": "\u5355\u4f4d\uff1a\u5ea6 / degrees",
        }
        for index, feature in enumerate([column for column in feature_columns if column != "MedInc"]):
            label = display_name(feature, field_descriptions, "bilingual")
            description = field_descriptions.get(feature, {}).get("description_zh", "")
            unit_hint = unit_hints.get(feature, "")
            with columns[index % 2]:
                values[feature] = st.number_input(
                    f"{label} | {unit_hint}",
                    value=float(defaults.get(feature, 0.0)),
                    help=description,
                )

        if st.button(ZH["predict_button"], type="primary"):
            input_data = pd.DataFrame([values], columns=feature_columns)
            raw_prediction = float(pipeline.predict(input_data)[0])
            rmb_prediction = float(values_to_display([raw_prediction], unit_config).iloc[0])
            usd_prediction = raw_prediction * 100000

            result_col_1, result_col_2, result_col_3 = st.columns(3)
            result_col_1.metric(ZH["raw_prediction"], f"{raw_prediction:.3f}", source_unit_label(unit_config))
            result_col_2.metric(ZH["usd_estimate"], f"${usd_prediction:,.0f}")
            result_col_3.metric(ZH["rmb_estimate"], f"{rmb_prediction:,.1f} \u4e07\u5143")

            st.info(ZH["rate_statement"].format(rate=exchange_rate))

            output_table = input_data.copy()
            output_table[ZH["raw_output"]] = raw_prediction
            output_table[ZH["display_output"].format(unit=display_unit_label(unit_config))] = rmb_prediction
            st.dataframe(output_table, use_container_width=True)

            csv_bytes = output_table.to_csv(index=False).encode("utf-8-sig")
            svg_bytes = build_prediction_svg(
                raw_prediction,
                usd_prediction,
                rmb_prediction,
                exchange_rate,
                importance,
            )
            download_col_1, download_col_2 = st.columns(2)
            download_col_1.download_button(
                ZH["download_csv"],
                data=csv_bytes,
                file_name="smarthouse_prediction.csv",
                mime="text/csv",
            )
            download_col_2.download_button(
                "\u4e0b\u8f7d\u9884\u6d4b\u6458\u8981\u900f\u660e SVG / Download summary SVG",
                data=svg_bytes,
                file_name="smarthouse_prediction_summary_transparent.svg",
                mime="image/svg+xml",
            )

        if not importance.empty:
            st.subheader(ZH["drivers"])
            render_feature_importance(importance)
            render_importance_charts(importance)
            bar_svg = build_importance_bar_svg(importance)
            donut_svg = build_importance_donut_svg(importance)
            chart_download_1, chart_download_2 = st.columns(2)
            chart_download_1.download_button(
                "\u4e0b\u8f7d\u6761\u5f62\u56fe\u900f\u660e SVG / Download bar chart SVG",
                data=bar_svg,
                file_name="feature_importance_bar_transparent.svg",
                mime="image/svg+xml",
            )
            chart_download_2.download_button(
                "\u4e0b\u8f7d\u73af\u5f62\u56fe\u900f\u660e SVG / Download donut chart SVG",
                data=donut_svg,
                file_name="feature_importance_donut_transparent.svg",
                mime="image/svg+xml",
            )
            st.caption(ZH["driver_caption"])

    with tab_model:
        st.subheader(ZH["model_perf"])
        current_model = bundle.get("model_type", config["model"]["type"])
        model_size_mb = model_path.stat().st_size / (1024 * 1024)

        cols = st.columns(4)
        cols[0].metric(ZH["current_model"], format_model_name(current_model))
        cols[1].metric("MAE", f"{metrics.get('mae', 0):.4f}")
        cols[2].metric("RMSE", f"{metrics.get('rmse', 0):.4f}")
        cols[3].metric("R2", f"{metrics.get('r2', 0):.4f}")
        st.caption(ZH["model_size"].format(size=model_size_mb))

        if not comparison.empty:
            comparison_display = comparison.copy()
            comparison_display["model"] = comparison_display["model"].map(format_model_name)
            st.dataframe(comparison_display, use_container_width=True)

    with tab_fields:
        st.subheader(ZH["field_dict"])
        rows = []
        for feature in feature_columns + [data_config["target_column"]]:
            item = field_descriptions.get(feature, {})
            rows.append(
                {
                    "\u539f\u5b57\u6bb5 / Raw Field": feature,
                    "\u4e2d\u6587\u540d\u79f0 / Chinese Name": item.get("zh_name", feature),
                    "English Name": item.get("en_name", feature),
                    "\u4e2d\u6587\u8bf4\u660e": item.get("description_zh", ""),
                    "English Description": item.get("description_en", ""),
                }
            )
        st.dataframe(pd.DataFrame(rows), use_container_width=True)


if __name__ == "__main__":
    main()

