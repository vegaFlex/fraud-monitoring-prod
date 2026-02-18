import pandas as pd
from pathlib import Path


RAW_PATH = Path("data/raw/creditcard.csv")
PROCESSED_PATH = Path("data/processed/transactions.parquet")


def main():
    print("Loading dataset...")

    df = pd.read_csv(RAW_PATH)

    # добавям transaction_id ако няма
    if "transaction_id" not in df.columns:
        df.insert(0, "transaction_id", range(1, len(df) + 1))

    # rename fraud label
    if "Class" in df.columns:
        df.rename(columns={"Class": "label"}, inplace=True)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(PROCESSED_PATH, index=False)

    print("Saved parquet dataset")
    print(df.head())


if __name__ == "__main__":
    main()
