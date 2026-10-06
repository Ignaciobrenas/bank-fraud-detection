import streamlit as st
import pandas as pd
from src.fraud_detection.config import CONFIG
from src.fraud_detection.analysis.kpi import calculate_financial_kpis
import os

st.set_page_config(layout="wide", page_title="Bank Fraud Detection Dashboard")
st.title("🛡️ Bank Fraud Detection Dashboard")
st.markdown("### Monitor in Real-Time")

# We will read alerts if they exist, otherwise fallback to features
alerts_path = "data/alerts.parquet"
if os.path.exists(alerts_path):
    df = pd.read_parquet(alerts_path)
    
    st.header("Business & Financial KPIs")
    kpis = calculate_financial_kpis(df, threshold_seconds=2.0)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Real-Time Detection", f"{kpis.get('real_time_detection_pct', 0):.1f}%")
    col2.metric("Precision", f"{kpis.get('precision_pct', 0):.1f}%")
    col3.metric("False Positive Rate", f"{kpis.get('false_positive_rate_pct', 0):.2f}%", delta_color="inverse")
    
    total_tx = len(df)
    col4.metric("Total Stream Txns", total_tx)
    
    st.markdown("---")
    st.header("Financial Impact")
    colA, colB, colC = st.columns(3)
    
    colA.metric("💰 Money Saved (Fraud Prevented)", f"${kpis.get('money_saved', 0):,.2f}")
    colB.metric("💸 Money Lost (Missed Fraud)", f"${kpis.get('money_lost_to_fraud', 0):,.2f}", delta_color="inverse")
    colC.metric("⚠️ Money Retained by Error (FPs)", f"${kpis.get('money_retained_error', 0):,.2f}", delta_color="inverse")
    
    st.markdown("---")
    st.subheader("Recent Alerts")
    st.dataframe(df[df["is_alert"] == 1].sort_values("event_timestamp", ascending=False).head(100))
    
else:
    st.warning("No alerts.parquet found. Please run the pipeline (`make stream`) first.")
