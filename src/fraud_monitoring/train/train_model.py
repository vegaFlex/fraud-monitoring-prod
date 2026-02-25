import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import roc_auc_score


FEATURES_PATH = Path("data/processed/features.parquet")
MODEL_PATH = Path("artifacts/model.joblib")


def main():
    print("Loading features dataset...")

    df = pd.read_parquet(FEATURES_PATH)

    drop_cols = ["transaction_id", "label"]
    X = df.drop(columns=drop_cols)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000))
    ])
              
    print("Training model...")
    pipeline.fit(X_train, y_train)

    proba = pipeline.predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, proba)

    print("ROC AUC:", auc)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipeline, MODEL_PATH)

    print("Model saved to:", MODEL_PATH)


if __name__ == "__main__":
    main()
