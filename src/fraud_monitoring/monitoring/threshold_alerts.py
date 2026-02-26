import pandas as pd
from sqlalchemy import create_engine, text

from src.fraud_monitoring.config.settings import load_settings


MEAN_PROBA_THRESHOLD = 0.02
TOTAL_EXPECTED_LOSS_THRESHOLD = 5000.0


def main():
    settings = load_settings()

    engine = create_engine(
        f"postgresql+psycopg2://{settings.postgres_user}:"
        f"{settings.postgres_password}@"
        f"{settings.postgres_host}:"
        f"{settings.postgres_port}/"
        f"{settings.postgres_db}"
    )

    with engine.connect() as conn:
        latest = pd.read_sql(
            text("""
                SELECT metric_name, metric_value
                FROM drift_metrics
                WHERE metric_name IN ('mean_fraud_proba', 'total_expected_loss')
                ORDER BY created_at DESC
            """),
            conn
        )

    mean_proba = latest.loc[latest["metric_name"] == "mean_fraud_proba", "metric_value"].head(1)
    total_loss = latest.loc[latest["metric_name"] == "total_expected_loss", "metric_value"].head(1)

    mean_proba_val = float(mean_proba.iloc[0]) if len(mean_proba) else 0.0
    total_loss_val = float(total_loss.iloc[0]) if len(total_loss) else 0.0

    alerts = []
    if mean_proba_val > MEAN_PROBA_THRESHOLD:
        alerts.append(("alert_mean_fraud_proba", mean_proba_val))

    if total_loss_val > TOTAL_EXPECTED_LOSS_THRESHOLD:
        alerts.append(("alert_total_expected_loss", total_loss_val))

    if alerts:
        alert_df = pd.DataFrame(
            [{"metric_name": name, "metric_value": val} for name, val in alerts]
        )

        engine = create_engine(
            f"postgresql+psycopg2://{settings.postgres_user}:"
            f"{settings.postgres_password}@"
            f"{settings.postgres_host}:"
            f"{settings.postgres_port}/"
            f"{settings.postgres_db}"
        )

        alert_df.to_sql("drift_metrics", engine, if_exists="append", index=False)

        print("ALERT triggered:", alerts)
    else:
        print("No alerts triggered.")


if __name__ == "__main__":
    main()