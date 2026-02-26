import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

from src.fraud_monitoring.config.settings import load_settings


FEATURES_PATH = Path("data/processed/features.parquet")


def main():
    settings = load_settings()

    df = pd.read_parquet(FEATURES_PATH)

    amount_mean = float(df["Amount"].mean())
    amount_std = float(df["Amount"].std())

    time_mean = float(df["Time"].mean())
    time_std = float(df["Time"].std())

    drift_data = pd.DataFrame([
        {"metric_name": "amount_mean", "metric_value": amount_mean},
        {"metric_name": "amount_std", "metric_value": amount_std},
        {"metric_name": "time_mean", "metric_value": time_mean},
        {"metric_name": "time_std", "metric_value": time_std},
    ])

    engine = create_engine(
        f"postgresql+psycopg2://{settings.postgres_user}:"
        f"{settings.postgres_password}@"
        f"{settings.postgres_host}:"
        f"{settings.postgres_port}/"
        f"{settings.postgres_db}"
    )

    drift_data.to_sql(
        "drift_metrics",
        engine,
        if_exists="append",
        index=False
    )

    print("Drift metrics saved.")


if __name__ == "__main__":
    main()