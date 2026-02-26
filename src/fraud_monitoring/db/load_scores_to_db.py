import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path

from src.fraud_monitoring.config.settings import load_settings


SCORES_PATH = Path("data/mart/scores.parquet")


def main():
    settings = load_settings()

    print("Loading scores parquet...")

    df = pd.read_parquet(SCORES_PATH)

    engine = create_engine(
        f"postgresql+psycopg2://{settings.postgres_user}:"
        f"{settings.postgres_password}@"
        f"{settings.postgres_host}:"
        f"{settings.postgres_port}/"
        f"{settings.postgres_db}"
    )

    print("Writing to PostgreSQL...")

    df[["transaction_id", "fraud_proba", "expected_loss", "risk_segment"]].to_sql(
        "scores",
        engine,
        if_exists="replace",
        index=False
    )

    print("Scores successfully loaded into database.")


if __name__ == "__main__":
    main()