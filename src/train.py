from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from data_loader import ensure_house_data, load_dataset
from evaluator import (
    plot_feature_importance,
    plot_predicted_vs_actual,
    regression_metrics,
    save_bilingual_predictions,
    save_metrics,
    save_predictions,
)
from field_metadata import display_name, load_field_descriptions
from model_comparison import compare_models
from models import build_model
from preprocessing import build_preprocessor
from reporter import build_report


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_config(root: Path) -> dict:
    return json.loads((root / "config.json").read_text(encoding="utf-8"))


def run_training() -> dict:
    root = project_root()
    config = load_config(root)
    data_config = config["data"]
    output_config = config["outputs"]
    presentation_config = config.get("presentation", {})
    unit_config = presentation_config.get("price_unit", {})
    field_descriptions = load_field_descriptions(root / presentation_config.get("field_descriptions_path", ""))

    csv_path = root / data_config["csv_path"]
    sample_path = root / data_config["sample_prediction_path"]
    data = ensure_house_data(csv_path, sample_path, data_config["target_column"])
    features, target = load_dataset(csv_path, data_config["target_column"])

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=data_config["test_size"],
        random_state=data_config["random_state"],
    )

    model_type = config["model"]["type"]
    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(features)),
            ("model", build_model(model_type)),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    metrics = regression_metrics(y_test, predictions)
    save_metrics(metrics, root / output_config["metrics_path"])
    save_predictions(y_test.to_numpy(), predictions, root / output_config["predictions_path"])
    save_bilingual_predictions(
        y_test.to_numpy(),
        predictions,
        root / output_config["predictions_bilingual_path"],
        unit_config,
    )
    plot_predicted_vs_actual(y_test.to_numpy(), predictions, root / output_config["plot_path"])
    feature_labels = [display_name(column, field_descriptions, "bilingual") for column in features.columns]
    plot_feature_importance(
        pipeline,
        features.columns.tolist(),
        root / output_config["feature_importance_path"],
        feature_labels,
    )

    bundle = {
        "pipeline": pipeline,
        "feature_columns": features.columns.tolist(),
        "target_column": data_config["target_column"],
        "model_type": model_type,
    }
    model_path = root / output_config["model_path"]
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, model_path, compress=3)
    model_size_mb = model_path.stat().st_size / (1024 * 1024)

    comparison = compare_models(x_train, x_test, y_train, y_test, root / output_config["model_comparison_path"])
    best_model = str(comparison.iloc[0]["model"]) if not comparison.empty else model_type

    build_report(
        dataset_name=data_config["dataset_name"],
        model_type=model_type,
        row_count=len(data),
        feature_count=features.shape[1],
        target_column=data_config["target_column"],
        feature_columns=features.columns.tolist(),
        field_descriptions=field_descriptions,
        metrics=metrics,
        unit_config=unit_config,
        model_size_mb=model_size_mb,
        best_model=best_model,
        report_path=root / output_config["report_path"],
    )

    return {"metrics": metrics, "model_size_mb": model_size_mb, "best_model": best_model}


if __name__ == "__main__":
    result = run_training()
    print("Training complete.")
    print(json.dumps(result, indent=2, ensure_ascii=False))
