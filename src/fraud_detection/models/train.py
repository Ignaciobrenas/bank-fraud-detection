import os
import json
import pandas as pd
from datetime import datetime
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report, average_precision_score
from src.fraud_detection.config import CONFIG, logger
import joblib

def run_train():
    logger.info("Starting model training...")
    gold_path = CONFIG["paths"]["gold"]
    if not os.path.exists(f"{gold_path}/features"):
        logger.error("No features in Gold. Run build_gold first.")
        return
        
    df = pd.read_parquet(f"{gold_path}/features")
    
    # Temporally split
    df = df.sort_values("event_timestamp")
    train_size = int(len(df) * 0.8)
    
    train = df.iloc[:train_size]
    test = df.iloc[train_size:]
    
    # We only use a subset of features for simplicity
    features = ["amount", "amount_zscore_customer", "age", "avg_monthly_spend"]
    
    X_train = train[features].fillna(0)
    y_train = train["is_fraud"]
    
    X_test = test[features].fillna(0)
    y_test = test["is_fraud"]
    
    clf = LGBMClassifier(class_weight="balanced", random_state=CONFIG["seed"], verbose=-1)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    y_prob = clf.predict_proba(X_test)[:, 1]
    
    pr_auc = average_precision_score(y_test, y_prob)
    logger.info("LightGBM Model Evaluation:")
    logger.info(f"\n{classification_report(y_test, y_pred)}")
    logger.info(f"PR-AUC: {pr_auc:.4f}")
    
    # Save Feature Importance
    importance_df = pd.DataFrame({
        "feature": features,
        "importance": clf.feature_importances_
    }).sort_values("importance", ascending=False)
    importance_df.to_csv("models/feature_importance.csv", index=False)
    logger.info("Feature importance saved to models/feature_importance.csv")
    
    # Save Metrics JSON
    metrics = {
        "training_time": datetime.utcnow().isoformat(),
        "pr_auc": float(pr_auc),
        "seed": CONFIG["seed"],
        "train_size": len(X_train),
        "test_size": len(X_test)
    }
    
    os.makedirs("models", exist_ok=True)
    with open("models/metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)
        
    joblib.dump(clf, "models/lgbm_model.pkl")
    logger.info("Model saved to models/lgbm_model.pkl")

if __name__ == "__main__":
    run_train()
