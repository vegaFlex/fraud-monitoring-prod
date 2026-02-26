from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from pathlib import Path


MODEL_PATH = Path("artifacts/model.joblib")

app = FastAPI(title="Fraud Monitoring API")

model = joblib.load(MODEL_PATH)


class TransactionInput(BaseModel):
    Time: float
    Amount: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float


@app.post("/score")
def score_transaction(tx: TransactionInput):

    df = pd.DataFrame([tx.model_dump()])

    # feature engineering същото като build_features.py
    df["amount_log"] = np.log1p(df["Amount"])
    df["hour"] = (df["Time"] // 3600) % 24
    df["day"] = df["Time"] // 86400
    df["high_amount_flag"] = (df["Amount"] > 2000).astype(int)

    # подреждане колоните както при training
    feature_order = model.feature_names_in_
    df = df[feature_order]

    fraud_proba = model.predict_proba(df)[0][1]
    expected_loss = fraud_proba * df["Amount"].iloc[0]

    if fraud_proba < 0.3:
        risk = "low"
    elif fraud_proba < 0.7:
        risk = "medium"
    else:
        risk = "high"

    return {
        "fraud_proba": float(fraud_proba),
        "expected_loss": float(expected_loss),
        "risk_segment": risk
    }