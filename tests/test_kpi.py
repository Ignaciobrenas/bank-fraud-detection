import pandas as pd
from src.fraud_detection.analysis.kpi import real_time_fraud_pct, calculate_financial_kpis

def test_real_time_fraud_pct_all_detected():
    df = pd.DataFrame({
        "is_fraud": [1, 1, 0],
        "is_alert": [1, 1, 0],
        "detection_latency_seconds": [1.0, 1.5, 0.5]
    })
    kpi = real_time_fraud_pct(df, 2.0)
    assert kpi == 100.0

def test_real_time_fraud_pct_late_detection():
    df = pd.DataFrame({
        "is_fraud": [1, 1],
        "is_alert": [1, 1],
        "detection_latency_seconds": [1.0, 3.0]
    })
    kpi = real_time_fraud_pct(df, 2.0)
    assert kpi == 50.0

def test_financial_kpis():
    df = pd.DataFrame({
        "is_fraud": [1, 1, 0, 0],
        "is_alert": [1, 0, 1, 0],
        "amount": [1000, 2000, 500, 100],
        "detection_latency_seconds": [1.0, 1.0, 1.0, 1.0]
    })
    kpis = calculate_financial_kpis(df, 2.0)
    
    assert kpis["money_saved"] == 1000       # TP
    assert kpis["money_lost_to_fraud"] == 2000 # FN
    assert kpis["money_retained_error"] == 500 # FP
    assert kpis["false_positive_rate_pct"] == 50.0 # 1 FP out of 2 negatives
    assert kpis["precision_pct"] == 50.0 # 1 TP, 1 FP
