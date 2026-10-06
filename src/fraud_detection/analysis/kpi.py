import pandas as pd
from typing import Dict, Any

def real_time_fraud_pct(alerts: pd.DataFrame, threshold_seconds: float) -> float:
    frauds = alerts[alerts["is_fraud"] == 1]
    if frauds.empty:
        return 0.0
    detected = frauds[
        (frauds["is_alert"] == 1)
        & (frauds["detection_latency_seconds"] <= threshold_seconds)
    ]
    return 100.0 * len(detected) / len(frauds)

def calculate_financial_kpis(alerts: pd.DataFrame, threshold_seconds: float) -> Dict[str, Any]:
    """Calculates advanced financial and performance KPIs."""
    if alerts.empty:
        return {}
        
    y_true = alerts["is_fraud"]
    y_pred = alerts["is_alert"]
    
    tp = alerts[(y_true == 1) & (y_pred == 1)]
    fp = alerts[(y_true == 0) & (y_pred == 1)]
    fn = alerts[(y_true == 1) & (y_pred == 0)]
    
    # Financial Impact (assuming an 'amount' column exists, otherwise fallback to counts)
    amount_col = "amount" if "amount" in alerts.columns else None
    
    money_saved = tp[amount_col].sum() if amount_col else len(tp) * 1000 # Dummy avg 1000
    money_lost = fn[amount_col].sum() if amount_col else len(fn) * 1000
    money_retained_fp = fp[amount_col].sum() if amount_col else len(fp) * 1000
    
    fpr = len(fp) / len(alerts[y_true == 0]) if len(alerts[y_true == 0]) > 0 else 0
    precision = len(tp) / (len(tp) + len(fp)) if (len(tp) + len(fp)) > 0 else 0
    
    return {
        "real_time_detection_pct": real_time_fraud_pct(alerts, threshold_seconds),
        "false_positive_rate_pct": fpr * 100,
        "precision_pct": precision * 100,
        "money_saved": float(money_saved),
        "money_lost_to_fraud": float(money_lost),
        "money_retained_error": float(money_retained_fp)
    }
