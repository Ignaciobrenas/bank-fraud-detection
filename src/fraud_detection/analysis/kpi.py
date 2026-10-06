import pandas as pd


def real_time_fraud_pct(alerts: pd.DataFrame, threshold_seconds: float) -> float:
    frauds = alerts[alerts["is_fraud"] == 1]
    if frauds.empty:
        return 0.0
    detected = frauds[
        (frauds["is_alert"] == 1)
        & (frauds["detection_latency_seconds"] <= threshold_seconds)
    ]
    return 100.0 * len(detected) / len(frauds)
