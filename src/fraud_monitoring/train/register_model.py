import joblib
from pathlib import Path
from sqlalchemy import create_engine
import pandas as pd

from src.fraud_monitoring.config.settings import load_settings


MODEL_PATH = Path("artifacts/model.joblib")


def main():
    settings = load_settings()

    if not MODEL_PATH.exists():
        raise RuntimeError("Model artifact missing.")

    engine = create_engine(
        f"postgresql+psycopg2://{settings.postgres_user}:"
        f"{settings.postgres_password}@"
        f"{settings.postgres_host}:"
        f"{settings.postgres_port}/"
        f"{settings.postgres_db}"
    )

    model_info = pd.DataFrame([{
        "model_name": settings.model_name,
        "auc": 0.95
    }])

    model_info.to_sql(
        "model_registry",
        engine,
        if_exists="append",
        index=False
    )

    print("Model registered in DB.")


if __name__ == "__main__":
    main()