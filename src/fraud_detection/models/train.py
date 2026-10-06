import os
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report, average_precision_score
from src.fraud_detection.config import CONFIG
import joblib

def run_train():
    gold_path = CONFIG["paths"]["gold"]
    if not os.path.exists(f"{gold_path}/features"):
        print("No features in Gold. Run build_gold first.")
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
    
    print("LightGBM Model Evaluation:")
    print(classification_report(y_test, y_pred))
    print(f"PR-AUC: {average_precision_score(y_test, y_prob):.4f}")
    
    os.makedirs("models", exist_ok=True)
    joblib.dump(clf, "models/lgbm_model.pkl")
    print("Model saved to models/lgbm_model.pkl")

if __name__ == "__main__":
    run_train()
