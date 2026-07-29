from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.datasets import fetch_california_housing


def ensure_house_data(csv_path: Path, sample_path: Path, target_column: str) -> pd.DataFrame:
    """Create a local teaching CSV if it does not exist yet."""
    if csv_path.exists():
        return pd.read_csv(csv_path)

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    sample_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        housing = fetch_california_housing(as_frame=True)
        data = housing.frame.rename(columns={"MedHouseVal": target_column})
    except Exception:
        data = _fallback_house_data(target_column)

    data.to_csv(csv_path, index=False)
    data.drop(columns=[target_column]).head(8).to_csv(sample_path, index=False)
    return data


def load_dataset(csv_path: Path, target_column: str) -> tuple[pd.DataFrame, pd.Series]:
    data = pd.read_csv(csv_path)
    if target_column not in data.columns:
        raise ValueError(f"Target column '{target_column}' was not found in {csv_path}.")

    features = data.drop(columns=[target_column])
    target = data[target_column]
    return features, target


def _fallback_house_data(target_column: str) -> pd.DataFrame:
    rows = []
    for index in range(600):
        rooms = 3 + (index % 7)
        bedrooms = 1 + (index % 4)
        population = 600 + (index % 90) * 18
        income = 2.0 + (index % 60) / 10
        house_age = 5 + (index % 45)
        latitude = 32.5 + (index % 30) / 10
        longitude = -124.0 + (index % 40) / 10
        price = (
            income * 0.42
            + rooms * 0.08
            - bedrooms * 0.04
            - house_age * 0.006
            + population * 0.00008
            + latitude * 0.015
            - abs(longitude + 120) * 0.03
        )
        rows.append(
            {
                "MedInc": round(income, 3),
                "HouseAge": house_age,
                "AveRooms": round(rooms, 3),
                "AveBedrms": round(bedrooms, 3),
                "Population": population,
                "AveOccup": round(2.1 + (index % 8) * 0.2, 3),
                "Latitude": round(latitude, 3),
                "Longitude": round(longitude, 3),
                target_column: round(price, 3),
            }
        )
    return pd.DataFrame(rows)
