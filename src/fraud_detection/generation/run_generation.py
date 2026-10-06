import pandas as pd
import numpy as np
from faker import Faker
import json
import os
from src.fraud_detection.config import CONFIG, logger

fake = Faker()
Faker.seed(CONFIG["seed"])
np.random.seed(CONFIG["seed"])

def generate_all():
    logger.info("Starting synthetic data generation...")
    raw_path = CONFIG["paths"]["raw"]
    os.makedirs(raw_path, exist_ok=True)
    
    n_cust = CONFIG["n_customers"]
    
    # 1. Customers
    customers = []
    for _ in range(n_cust):
        customers.append({
            "customer_id": f"c-{fake.uuid4()[:8]}",
            "age": np.random.randint(18, 80),
            "country": fake.country_code(),
            "home_city": fake.city(),
            "home_lat": float(fake.latitude()),
            "home_lon": float(fake.longitude()),
            "risk_level": np.random.choice(["low", "medium", "high"], p=[0.7, 0.2, 0.1]),
            "account_open_date": fake.date_between(start_date="-5y", end_date="today").isoformat(),
            "avg_monthly_spend": float(np.round(np.random.lognormal(mean=5, sigma=1), 2))
        })
    df_cust = pd.DataFrame(customers)
    df_cust.to_csv(f"{raw_path}/customer_profile.csv", index=False)
    
    # 2. Devices
    devices = []
    for c in customers:
        num_devices = np.random.randint(1, 4)
        for _ in range(num_devices):
            devices.append({
                "device_id": f"d-{fake.uuid4()[:8]}",
                "customer_id": c["customer_id"],
                "device_type": np.random.choice(["mobile", "web"]),
                "os": "Android" if np.random.rand() > 0.5 else "iOS",
                "browser": "Chrome",
                "app_version": "1.0.0",
                "first_seen": fake.date_time_between(start_date="-1y", end_date="now").isoformat() + "Z",
                "is_rooted": bool(np.random.rand() > 0.95)
            })
    with open(f"{raw_path}/device_data.json", "w") as f:
        json.dump(devices, f)
        
    # 3. Transactions (History + Stream combined for generation, split later)
    # We will generate just 1000 transactions to save time for this simplified version, unless we want the full n_history
    n_hist = min(CONFIG["n_history_transactions"], 10000)
    n_stream = min(CONFIG["n_stream_transactions"], 2000)
    
    transactions = []
    locations = []
    alerts = []
    access_logs = []
    
    # Generate simple transactions
    all_devices = pd.DataFrame(devices)
    
    for i in range(n_hist + n_stream):
        cust = np.random.choice(customers)
        cust_id = cust["customer_id"]
        cust_devs = all_devices[all_devices["customer_id"] == cust_id]
        if cust_devs.empty:
            dev_id = f"d-{fake.uuid4()[:8]}"
        else:
            dev_id = cust_devs.iloc[0]["device_id"]
            
        is_fraud = 1 if np.random.rand() < CONFIG["fraud_rate"] else 0
        fraud_type = np.random.choice(["impossible_travel", "new_device_high_amount", "velocity_burst", "account_takeover", "foreign_country"]) if is_fraud else ""
        
        ts = fake.date_time_between(start_date="-6m", end_date="now").isoformat() + "Z"
        txn_id = f"t-{fake.uuid4()[:8]}"
        
        transactions.append({
            "transaction_id": txn_id,
            "customer_id": cust_id,
            "source_account": f"acc-{fake.uuid4()[:8]}",
            "destination_account": f"acc-{fake.uuid4()[:8]}",
            "amount": float(np.round(np.random.lognormal(mean=4, sigma=1) if not is_fraud else np.random.lognormal(mean=7, sigma=1), 2)),
            "currency": "EUR",
            "merchant_category": "retail",
            "channel": "mobile",
            "device_id": dev_id,
            "event_timestamp": ts,
            "is_fraud": is_fraud,
            "fraud_type": fraud_type
        })
        
        locations.append({
            "transaction_id": txn_id,
            "customer_id": cust_id,
            "ip_address": fake.ipv4(),
            "ip_country": cust["country"] if fraud_type != "foreign_country" else fake.country_code(),
            "gps": {"lat": float(fake.latitude()), "lon": float(fake.longitude())},
            "event_timestamp": ts
        })
        
        if np.random.rand() < 0.1:
            access_logs.append({
                "event_id": f"e-{fake.uuid4()[:8]}",
                "customer_id": cust_id,
                "event_type": "login_failed" if fraud_type == "account_takeover" else "login_success",
                "event_timestamp": ts,
                "device_id": dev_id,
                "ip_address": fake.ipv4(),
                "user_agent": fake.user_agent(),
                "geo": {"country": cust["country"], "city": cust["home_city"]}
            })
            
    df_tx = pd.DataFrame(transactions)
    df_tx = df_tx.sort_values("event_timestamp")
    
    df_hist = df_tx.iloc[:n_hist]
    df_stream = df_tx.iloc[n_hist:]
    
    df_hist.to_parquet(f"{raw_path}/transaction_history.parquet", index=False)
    df_stream.to_csv(f"{raw_path}/transactions.csv", index=False)
    
    with open(f"{raw_path}/user_location.json", "w") as f:
        json.dump(locations, f)
        
    with open(f"{raw_path}/access_logs.jsonl", "w") as f:
        for log in access_logs:
            f.write(json.dumps(log) + "\n")
            
    # Alerts
    for _, row in df_hist[df_hist["is_fraud"] == 1].head(100).iterrows():
        alerts.append({
            "alert_id": f"a-{fake.uuid4()[:8]}",
            "customer_id": row["customer_id"],
            "transaction_id": row["transaction_id"],
            "alert_timestamp": row["event_timestamp"],
            "alert_type": "high_risk",
            "resolution": "confirmed"
        })
    pd.DataFrame(alerts).to_csv(f"{raw_path}/previous_fraud_alerts.csv", index=False)
    logger.info("Generation complete!")

if __name__ == "__main__":
    generate_all()
