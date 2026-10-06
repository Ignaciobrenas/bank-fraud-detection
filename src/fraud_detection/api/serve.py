from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import os
from src.fraud_detection.config import logger

app = FastAPI(title="Bank Fraud Detection Inference API", version="1.0.0")

# Load model at startup
MODEL_PATH = "models/lgbm_model.pkl"
clf = None

if os.path.exists(MODEL_PATH):
    clf = joblib.load(MODEL_PATH)
    logger.info("Loaded LightGBM model for API inference.")
else:
    logger.warning("Model not found at startup. API will return 503 until model is trained.")

class TransactionInput(BaseModel):
    transaction_id: str
    customer_id: str
    amount: float
    amount_zscore_customer: float
    age: int
    avg_monthly_spend: float

class FraudPredictionResponse(BaseModel):
    transaction_id: str
    is_alert: bool
    fraud_score: float

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": clf is not None}

@app.post("/predict", response_model=FraudPredictionResponse)
def predict_fraud(transaction: TransactionInput):
    if clf is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")
    
    # Extract features in the order expected by the model
    features = ["amount", "amount_zscore_customer", "age", "avg_monthly_spend"]
    df_features = pd.DataFrame([[
        transaction.amount,
        transaction.amount_zscore_customer,
        transaction.age,
        transaction.avg_monthly_spend
    ]], columns=features)
    
    score = float(clf.predict_proba(df_features)[0, 1])
    is_alert = score > 0.5
    
    logger.info(f"Scored transaction {transaction.transaction_id}: {score:.4f} (Alert: {is_alert})")
    
    return FraudPredictionResponse(
        transaction_id=transaction.transaction_id,
        is_alert=is_alert,
        fraud_score=score
    )
