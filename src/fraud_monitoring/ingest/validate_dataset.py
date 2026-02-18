import pandas as pd
from pathlib import Path


PARQUET_PATH = Path("data/processed/transactions.parquet")


def main():
    df = pd.read_parquet(PARQUET_PATH)

    required_cols = {"transaction_id", "Time", "Amount", "label"}
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    if df["transaction_id"].isna().any():
        raise ValueError("transaction_id contains nulls")

    if df["transaction_id"].duplicated().any():
        raise ValueError("transaction_id contains duplicates")

    if df["Amount"].isna().any():
        raise ValueError("Amount contains nulls")

    if df["Time"].isna().any():
        raise ValueError("Time contains nulls")

    if not set(df["label"].unique()).issubset({0, 1}):
        raise ValueError("label must be 0/1")

    if (df["Amount"] < 0).any():
        raise ValueError("Amount contains negative values")

    print("Validation OK")
    print("Rows:", len(df))
    print("Fraud rate:", float(df["label"].mean()))
    print("Amount min/max:", float(df["Amount"].min()), float(df["Amount"].max()))
    print("Time min/max:", float(df["Time"].min()), float(df["Time"].max()))


if __name__ == "__main__":
    main()
