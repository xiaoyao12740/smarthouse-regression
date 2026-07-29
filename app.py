from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from field_metadata import display_name, load_field_descriptions
from price_units import display_unit_label, source_unit_label, values_to_display


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
        "random_forest": "随机森林 / Random Forest",
        "ridge": "岭回归 / Ridge Regression",
        "linear_regression": "线性回归 / Linear Regression",
    }
    return names.get(name, name)


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
                "影响因素 / Feature": display_name(feature, field_descriptions, "bilingual"),
                "重要性 / Importance": float(importance),
            }
        )
    return pd.DataFrame(rows).sort_values("重要性 / Importance", ascending=False)


def main() -> None:
    st.set_page_config(page_title="SmartHouse AI Predictor", page_icon="House", layout="wide")

    config = load_config()
    data_config = config["data"]
    output_config = config["outputs"]
    presentation_config = config.get("presentation", {})
    unit_config = presentation_config.get("price_unit", {})
    field_descriptions = load_field_descriptions(PROJECT_ROOT / presentation_config.get("field_descriptions_path", ""))
    exchange_rate = unit_config.get("usd_to_rmb", 6.6)

    st.title("SmartHouse AI Predictor / 智能房价预测")
    st.caption(
        "基于 California Housing 数据集的回归预测演示。人民币结果按固定假设 "
        f"1 USD = {exchange_rate} RMB 换算，仅用于作品展示。"
    )

    model_path = PROJECT_ROOT / output_config["model_path"]
    if not model_path.exists():
        st.error("未找到已训练模型。请先运行训练脚本生成 models/house_price_model.joblib。")
        return

    bundle = load_model(output_config["model_path"])
    feature_columns = bundle["feature_columns"]
    pipeline = bundle["pipeline"]
    metrics = load_metrics(output_config["metrics_path"])
    comparison = load_comparison(output_config["model_comparison_path"])
    importance = feature_importance_table(bundle, field_descriptions)

    tab_predict, tab_model, tab_fields = st.tabs(
        ["房价预测 / Prediction", "模型信息 / Model", "字段说明 / Fields"]
    )

    with tab_predict:
        st.subheader("输入房屋区域特征 / Enter House Area Features")
        defaults = {
            "MedInc": 5.0,
            "HouseAge": 25.0,
            "AveRooms": 5.5,
            "AveBedrms": 1.1,
            "Population": 1200.0,
            "AveOccup": 2.8,
            "Latitude": 34.0,
            "Longitude": -118.0,
        }

        values = {}
        columns = st.columns(2)
        for index, feature in enumerate(feature_columns):
            label = display_name(feature, field_descriptions, "bilingual")
            description = field_descriptions.get(feature, {}).get("description_zh", "")
            with columns[index % 2]:
                values[feature] = st.number_input(
                    label,
                    value=float(defaults.get(feature, 0.0)),
                    help=description,
                )

        if st.button("预测房价 / Predict Price", type="primary"):
            input_data = pd.DataFrame([values], columns=feature_columns)
            raw_prediction = float(pipeline.predict(input_data)[0])
            rmb_prediction = float(values_to_display([raw_prediction], unit_config).iloc[0])
            usd_prediction = raw_prediction * 100000

            result_col_1, result_col_2, result_col_3 = st.columns(3)
            result_col_1.metric("原始预测 / Raw", f"{raw_prediction:.3f}", source_unit_label(unit_config))
            result_col_2.metric("美元估算 / USD", f"${usd_prediction:,.0f}")
            result_col_3.metric("人民币估算 / RMB", f"{rmb_prediction:,.1f} 万元")

            st.info(
                f"汇率声明：人民币展示按固定假设 1 USD = {exchange_rate} RMB 换算，"
                "用于项目展示和直观理解，不代表实时汇率或真实中国房价数据。"
            )

            output_table = input_data.copy()
            output_table["预测房价原始值 / Raw prediction (100k USD)"] = raw_prediction
            output_table[f"预测房价 / Predicted price ({display_unit_label(unit_config)})"] = rmb_prediction
            st.dataframe(output_table, use_container_width=True)

        if not importance.empty:
            st.subheader("主要影响因素 / Key Drivers")
            st.bar_chart(importance.set_index("影响因素 / Feature"))
            st.caption("这里使用随机森林的 feature_importances_，用于提供一个轻量级模型解释。")

    with tab_model:
        st.subheader("模型表现 / Model Performance")
        current_model = bundle.get("model_type", config["model"]["type"])
        model_size_mb = model_path.stat().st_size / (1024 * 1024)

        cols = st.columns(4)
        cols[0].metric("当前模型 / Model", format_model_name(current_model))
        cols[1].metric("MAE", f"{metrics.get('mae', 0):.4f}")
        cols[2].metric("RMSE", f"{metrics.get('rmse', 0):.4f}")
        cols[3].metric("R2", f"{metrics.get('r2', 0):.4f}")
        st.caption(f"模型文件大小 / Model file size: {model_size_mb:.2f} MB")

        if not comparison.empty:
            comparison_display = comparison.copy()
            comparison_display["model"] = comparison_display["model"].map(format_model_name)
            st.dataframe(comparison_display, use_container_width=True)

    with tab_fields:
        st.subheader("字段词典 / Field Dictionary")
        rows = []
        for feature in feature_columns + [data_config["target_column"]]:
            item = field_descriptions.get(feature, {})
            rows.append(
                {
                    "原字段 / Raw Field": feature,
                    "中文名称 / Chinese Name": item.get("zh_name", feature),
                    "English Name": item.get("en_name", feature),
                    "中文说明": item.get("description_zh", ""),
                    "English Description": item.get("description_en", ""),
                }
            )
        st.dataframe(pd.DataFrame(rows), use_container_width=True)


if __name__ == "__main__":
    main()
