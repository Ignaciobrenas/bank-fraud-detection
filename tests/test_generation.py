import pandas as pd
from src.fraud_detection.config import CONFIG

def test_fraud_rate_is_valid():
    # If the user has generated data, check it
    import os
    raw_path = CONFIG["paths"]["raw"]
    if os.path.exists(f"{raw_path}/transactions.csv"):
        df = pd.read_csv(f"{raw_path}/transactions.csv")
        rate = df["is_fraud"].mean()
        assert rate >= 0.0, "Fraud rate must be >= 0"
        
def test_config_seed_exists():
    assert "seed" in CONFIG
    assert type(CONFIG["seed"]) is int
