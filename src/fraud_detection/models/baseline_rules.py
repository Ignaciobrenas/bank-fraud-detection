import os
import pandas as pd
from src.fraud_detection.config import CONFIG

def evaluate_baseline():
    gold_path = CONFIG["paths"]["gold"]
    if not os.path.exists(f"{gold_path}/features"):
        print("No features in Gold. Run build_gold first.")
        return
        
    df = pd.read_parquet(f"{gold_path}/features")
    
    # Simple rule: if amount > 5000 or amount_zscore_customer > 3 -> alert
    df["baseline_alert"] = ((df["amount"] > 5000) | (df["amount_zscore_customer"] > 3)).astype(int)
    
    # Evaluate
    y_true = df["is_fraud"]
    y_pred = df["baseline_alert"]
    
    tp = sum((y_true == 1) & (y_pred == 1))
    fp = sum((y_true == 0) & (y_pred == 1))
    fn = sum((y_true == 1) & (y_pred == 0))
    
    precision = tp / (tp + fp) if tp + fp > 0 else 0
    recall = tp / (tp + fn) if tp + fn > 0 else 0
    
    print("Baseline Rules Evaluation:")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"TP: {tp}, FP: {fp}, FN: {fn}")

if __name__ == "__main__":
    evaluate_baseline()
