import pandas as pd
from src.fraud_detection.analysis.kpi import real_time_fraud_pct
import os

def analyze_scenarios():
    if not os.path.exists("data/alerts.parquet"):
        print("Alerts data not found. Run streaming consumer first.")
        return
        
    alerts = pd.read_parquet("data/alerts.parquet")
    
    # Scenario A: Batch rules (latency > 3600)
    alerts_a = alerts.copy()
    alerts_a["detection_latency_seconds"] = 3600 
    kpi_a = real_time_fraud_pct(alerts_a, 2.0)
    
    # Scenario B: Stream rules (latency < 2, but logic is rules)
    alerts_b = alerts.copy()
    alerts_b["detection_latency_seconds"] = 1.0
    alerts_b["is_alert"] = (alerts_b["fraud_score"] > 0.8).astype(int)
    kpi_b = real_time_fraud_pct(alerts_b, 2.0)
    
    # Scenario C: Stream ML (what we have)
    kpi_c = real_time_fraud_pct(alerts, 2.0)
    
    print("--- KPI Scenarios ---")
    print(f"Scenario A (Batch Rules): {kpi_a:.2f}%")
    print(f"Scenario B (Stream Rules): {kpi_b:.2f}%")
    print(f"Scenario C (Stream ML): {kpi_c:.2f}%")

if __name__ == "__main__":
    analyze_scenarios()
