import os
import pandas as pd
import joblib
from src.fraud_detection.config import CONFIG, logger

def run_consumer():
    logger.info("Starting Streaming Consumer...")
    raw_path = CONFIG["paths"]["raw"]
    
    if not os.path.exists(f"{raw_path}/transactions.csv"):
        logger.error("No stream transactions found.")
        return
        
    df_stream = pd.read_csv(f"{raw_path}/transactions.csv")
    
    if not os.path.exists("models/lgbm_model.pkl"):
        logger.error("Model not found. Run train.py first.")
        return
        
    clf = joblib.load("models/lgbm_model.pkl")
    
    # Simulated feature calculation for stream
    df_stream["amount_zscore_customer"] = 0 
    df_stream["age"] = 30 
    df_stream["avg_monthly_spend"] = 1000 
    
    features = ["amount", "amount_zscore_customer", "age", "avg_monthly_spend"]
    X_score = df_stream[features].fillna(0)
    
    scores = clf.predict_proba(X_score)[:, 1]
    df_stream["fraud_score"] = scores
    df_stream["is_alert"] = (scores > 0.5).astype(int)
    
    # Simulating latency of 1.5 seconds
    df_stream["detection_latency_seconds"] = 1.5 
    
    alerts = df_stream[["transaction_id", "event_timestamp", "is_alert", "fraud_score", "detection_latency_seconds", "is_fraud"]]
    
    os.makedirs("data", exist_ok=True)
    alerts.to_parquet("data/alerts.parquet", index=False)
    logger.info("Streaming consumer generated alerts.parquet")

if __name__ == "__main__":
    run_consumer()
