from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from price_units import display_unit_label, source_unit_label, values_to_display

plt.rcParams["font.sans-serif"] = [
    "Microsoft YaHei",
    "SimHei",
    "Noto Sans CJK SC",
    "Arial Unicode MS",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False


def regression_metrics(y_true, predictions) -> dict:
    mse = mean_squared_error(y_true, predictions)
    return {
        "mae": float(mean_absolute_error(y_true, predictions)),
        "rmse": float(np.sqrt(mse)),
        "r2": float(r2_score(y_true, predictions)),
    }


def save_metrics(metrics: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(metrics, indent=2, ensure_ascii=False), encoding="utf-8")


def save_predictions(y_true, predictions, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame({"actual": y_true, "prediction": predictions, "error": predictions - y_true}).to_csv(
        path, index=False
    )


def save_bilingual_predictions(y_true, predictions, path: Path, unit_config: dict) -> None:
    actual_display = values_to_display(y_true, unit_config)
    predicted_display = values_to_display(predictions, unit_config)
    display_unit = display_unit_label(unit_config)
    source_unit = source_unit_label(unit_config)

    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(
        {
            f"真实房价 / Actual price ({display_unit})": actual_display,
            f"预测房价 / Predicted price ({display_unit})": predicted_display,
            f"预测误差 / Error ({display_unit})": predicted_display - actual_display,
            f"真实房价原始值 / Raw actual ({source_unit})": y_true,
            f"预测房价原始值 / Raw prediction ({source_unit})": predictions,
        }
    ).to_csv(path, index=False, encoding="utf-8-sig")


def plot_predicted_vs_actual(y_true, predictions, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(7, 6))
    plt.scatter(y_true, predictions, alpha=0.35, edgecolors="none")
    min_value = min(float(np.min(y_true)), float(np.min(predictions)))
    max_value = max(float(np.max(y_true)), float(np.max(predictions)))
    plt.plot([min_value, max_value], [min_value, max_value], color="crimson", linewidth=2)
    plt.xlabel("Actual price / 真实房价")
    plt.ylabel("Predicted price / 预测房价")
    plt.title("Predicted vs Actual House Price / 预测值与真实值对比")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def plot_feature_importance(
    pipeline, feature_columns: list[str], path: Path, feature_labels: list[str] | None = None
) -> bool:
    model = pipeline.named_steps["model"]
    if not hasattr(model, "feature_importances_"):
        return False

    path.parent.mkdir(parents=True, exist_ok=True)
    importances = model.feature_importances_
    order = np.argsort(importances)[-10:]
    label_source = feature_labels if feature_labels else feature_columns
    labels = [label_source[index] for index in order]

    plt.figure(figsize=(8, 5))
    plt.barh(labels, importances[order], color="#2f6f73")
    plt.xlabel("Importance / 重要性")
    plt.title("Top Feature Importance / 主要影响因素")
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()
    return True
