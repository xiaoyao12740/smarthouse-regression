from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.pipeline import Pipeline

from evaluator import regression_metrics
from models import available_models, build_model
from preprocessing import build_preprocessor


def compare_models(x_train, x_test, y_train, y_test, output_path: Path) -> pd.DataFrame:
    records = []
    for model_type in available_models():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor(x_train)),
                ("model", build_model(model_type)),
            ]
        )
        pipeline.fit(x_train, y_train)
        predictions = pipeline.predict(x_test)
        metrics = regression_metrics(y_test, predictions)
        records.append({"model": model_type, **metrics})

    comparison = pd.DataFrame(records).sort_values(["r2", "rmse"], ascending=[False, True])
    output_path.parent.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(output_path, index=False, encoding="utf-8-sig")
    return comparison
