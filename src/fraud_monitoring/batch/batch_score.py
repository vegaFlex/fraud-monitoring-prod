import pandas as pd
import joblib
from pathlib import Path


FEATURES_PATH = Path("data/processed/features.parquet")
MODEL_PATH = Path("artifacts/model.joblib")
OUTPUT_PATH = Path("data/mart/scores.parquet")


def main():
    print("Loading features...")

    df = pd.read_parquet(FEATURES_PATH)
    model = joblib.load(MODEL_PATH)

    X = df.drop(columns=["transaction_id", "label"])

    print("Scoring transactions...")
    fraud_proba = model.predict_proba(X)[:, 1]

    df["fraud_proba"] = fraud_proba

    # expected financial loss
    df["expected_loss"] = df["fraud_proba"] * df["Amount"]

    # risk segment
    df["risk_segment"] = pd.cut(
        df["fraud_proba"],
        bins=[-1, 0.3, 0.7, 1],
        labels=["low", "medium", "high"]
    )

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    print("Scores saved")
    print(df[["transaction_id", "fraud_proba", "expected_loss", "risk_segment"]].head())


if __name__ == "__main__":
    main()