from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd

from field_metadata import load_field_descriptions, rename_columns_for_display
from price_units import display_unit_label, values_to_display


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_config(root: Path) -> dict:
    return json.loads((root / "config.json").read_text(encoding="utf-8"))


def predict(input_path: Path | None = None) -> Path:
    root = project_root()
    config = load_config(root)
    data_config = config["data"]
    output_config = config["outputs"]
    presentation_config = config.get("presentation", {})
    unit_config = presentation_config.get("price_unit", {})
    field_descriptions = load_field_descriptions(root / presentation_config.get("field_descriptions_path", ""))

    model_path = root / output_config["model_path"]
    if not model_path.exists():
        raise FileNotFoundError("Model file was not found. Please run training first.")

    bundle = joblib.load(model_path)
    feature_columns = bundle["feature_columns"]
    pipeline = bundle["pipeline"]

    source = input_path if input_path else root / data_config["sample_prediction_path"]
    data = pd.read_csv(source)
    missing = [column for column in feature_columns if column not in data.columns]
    if missing:
        raise ValueError(f"Prediction data is missing required columns: {missing}")

    predictions = pipeline.predict(data[feature_columns])
    result = data.copy()
    result["predicted_median_house_value"] = predictions
    result["predicted_price_10k_rmb"] = values_to_display(predictions, unit_config)

    output_path = root / output_config["prediction_output_path"]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    bilingual_output_path = root / output_config["prediction_bilingual_output_path"]
    bilingual_columns = rename_columns_for_display(result.columns.tolist(), field_descriptions)
    bilingual_columns["predicted_median_house_value"] = "预测房价原始值 / Raw predicted median house value (100k USD)"
    bilingual_columns["predicted_price_10k_rmb"] = f"预测房价 / Predicted price ({display_unit_label(unit_config)})"
    result.rename(columns=bilingual_columns).to_csv(bilingual_output_path, index=False, encoding="utf-8-sig")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default=None, help="CSV file for prediction.")
    args = parser.parse_args()
    path = predict(Path(args.input) if args.input else None)
    print(f"Prediction saved to: {path}")
