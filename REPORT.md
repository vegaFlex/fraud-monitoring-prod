# Fraud Monitoring Production System Report

## 1. Project Overview

This project builds a production-ready fraud monitoring system designed to detect high-risk financial transactions and estimate expected financial loss in real time.

The system combines machine learning, API scoring, monitoring, and business intelligence reporting.

Main objectives:

- Predict fraud probability for each transaction
- Estimate expected financial loss
- Segment transactions by risk level
- Enable monitoring and model lifecycle management
- Provide business-ready dashboards

---

## 2. Data Source

Dataset: Credit Card Fraud Detection (OpenML)

The dataset contains anonymized transaction features:

- Time — seconds elapsed between transactions
- Amount — transaction value
- V1–V28 — PCA-transformed confidential features
- Class — fraud label (used only during training)

Highly imbalanced dataset where fraud transactions represent a very small percentage of total transactions.

---

## 3. Modeling Approach

### Feature Processing
- Standard scaling applied to numerical features
- Train/Test split with stratification

### Model
Logistic Regression baseline model was selected for:

- interpretability
- stability
- fast inference
- production suitability

### Output Metrics
Model produces:

- fraud_proba — probability transaction is fraud
- expected_loss — estimated financial risk
- risk_segment:
  - low
  - medium
  - high

Expected loss calculation:

expected_loss = fraud_probability × transaction_amount

---

## 4. Production Architecture

The system simulates a real ML production environment.

Pipeline components:

1. Data ingestion
2. Feature generation
3. Model training
4. Batch scoring
5. FastAPI realtime scoring endpoint
6. PostgreSQL risk mart
7. Monitoring layer
8. Power BI dashboard

Database tables:

- transactions_raw
- features
- scores
- drift_metrics
- model_registry

---

## 5. Monitoring and Model Stability

### Data Drift Monitoring
Tracks distribution changes for:
- transaction amount
- transaction time

### Prediction Drift
Monitors average fraud probability over time.

### Alerts
Automatic alerts triggered when expected financial loss exceeds threshold.

Example alert detected elevated expected loss requiring investigation.

---

## 6. Business Insights

Key findings from scoring results:

- Majority of transactions fall into low-risk segment.
- Small subset of transactions drives disproportionate financial risk.
- Expected loss KPI allows prioritization of investigations.
- High-risk transactions identified using probability and loss together.

This enables fraud teams to focus investigation resources efficiently.

---

## 7. Dashboard Capabilities

Power BI dashboard provides:

- Total expected financial loss KPI
- Risk distribution visualization
- Fraud probability trend monitoring
- Top risky transactions table

Designed for fraud analysts and risk managers.

---

## 8. Model Lifecycle Management

Implemented lifecycle features:

- model version registration
- monitoring metrics storage
- retraining readiness
- production scoring API

Supports continuous improvement workflow.

---

## 9. Limitations

- Dataset is anonymized (no behavioral features).
- No real-time streaming source.
- Thresholds manually defined.

---

## 10. Future Improvements

- automated retraining scheduling
- advanced models (Gradient Boosting)
- feature store implementation
- real-time alert notifications

---

## 11. Conclusion

The project demonstrates an end-to-end fraud monitoring system covering machine learning, production deployment, monitoring, and business analytics integration.

The architecture reflects real industry fraud detection workflows.