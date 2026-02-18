import pandas as pd
import numpy as np
from pathlib import Path


INPUT_PATH = Path("data/processed/transactions.parquet")
OUTPUT_PATH = Path("data/processed/features.parquet")


def main():
    print("Loading transactions dataset...")

    df = pd.read_parquet(INPUT_PATH)

    # amount features
    df["amount_log"] = np.log1p(df["Amount"])

    # time features
    df["hour"] = (df["Time"] // 3600) % 24
    df["day"] = df["Time"] // 86400

    # basic risk flag
    df["high_amount_flag"] = (df["Amount"] > 2000).astype(int)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(OUTPUT_PATH, index=False)

    print("Features saved")
    print(df.head())


if __name__ == "__main__":
    main()
