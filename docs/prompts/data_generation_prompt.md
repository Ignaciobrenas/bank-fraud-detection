You are a data engineer at a retail bank. Design and write a Python 3.11 generator
for synthetic data to build a real-time fraud detection pipeline.

Datasets: transactions, transaction_history, customer_profile, access_logs (JSON Lines),
user_location (JSON), device_data (JSON), previous_fraud_alerts.

Requirements:
- Reproducible with a fixed seed.
- Configurable via a YAML file: number of customers, number of transactions, fraud rate.
- Fraud rate between 0.5% and 2%, with an is_fraud label and a fraud_type column.
- Inject these fraud patterns: impossible_travel, new_device_high_amount,
  velocity_burst, account_takeover, foreign_country.
- Include hard fraud cases that look similar to normal behavior.
- Realistic distributions: log-normal amounts, daily and weekly seasonality.
- Foreign keys must be consistent across datasets.
- previous_fraud_alerts must only reference the historical period.
- All code, variable names and column names in English, no comments.
- Output files: CSV for tabular data, JSON/JSONL for semi-structured data.
