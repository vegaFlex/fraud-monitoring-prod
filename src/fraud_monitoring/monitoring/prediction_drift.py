import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

from src.fraud_monitoring.config.settings import load_settings


SCORES_PATH = Path("data/mart/scores.parquet")


def main():
    settings = load_settings()

    df = pd.read_parquet(SCORES_PATH)

    mean_proba = float(df["fraud_proba"].mean())
    high_risk_ratio = float((df["risk_segment"] == "high").mean())
    total_expected_loss = float(df["expected_loss"].sum())

    drift_data = pd.DataFrame([
        {"metric_name": "mean_fraud_proba", "metric_value": mean_proba},
        {"metric_name": "high_risk_ratio", "metric_value": high_risk_ratio},
        {"metric_name": "total_expected_loss", "metric_value": total_expected_loss},
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

    print("Prediction drift metrics saved.")


if __name__ == "__main__":
    main()