from __future__ import annotations

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge


def build_model(model_type: str):
    if model_type == "linear_regression":
        return LinearRegression()
    if model_type == "ridge":
        return Ridge(alpha=1.0, random_state=42)
    if model_type == "random_forest":
        return RandomForestRegressor(
            n_estimators=80,
            max_depth=16,
            min_samples_split=4,
            random_state=42,
            n_jobs=-1,
        )

    raise ValueError(
        f"Unsupported model type '{model_type}'. "
        "Choose from: linear_regression, ridge, random_forest."
    )


def available_models() -> list[str]:
    return ["linear_regression", "ridge", "random_forest"]
