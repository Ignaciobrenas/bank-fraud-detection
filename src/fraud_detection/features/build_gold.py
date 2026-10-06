import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean, stddev
from pyspark.sql.window import Window
from src.fraud_detection.config import CONFIG, logger

def run_build_gold():
    logger.info("Starting Gold layer feature engineering...")
    spark = SparkSession.builder \
        .appName("BankFraud_BuildGold") \
        .master("local[*]") \
        .getOrCreate()
        
    silver_path = CONFIG["paths"]["silver"]
    gold_path = CONFIG["paths"]["gold"]
    
    if not os.path.exists(f"{silver_path}/transactions"):
        logger.error("No transactions in Silver. Run build_silver first.")
        return
        
    df_tx = spark.read.parquet(f"{silver_path}/transactions")
    
    # Feature Engineering (Simple)
    window_cust = Window.partitionBy("customer_id")
    df_gold = df_tx.withColumn("mean_amount", mean("amount").over(window_cust)) \
                   .withColumn("std_amount", stddev("amount").over(window_cust))
                   
    df_gold = df_gold.withColumn("amount_zscore_customer", (col("amount") - col("mean_amount")) / (col("std_amount") + 1e-5))
    
    if os.path.exists(f"{silver_path}/customer_profile"):
        df_cust = spark.read.parquet(f"{silver_path}/customer_profile").select(
            "customer_id", "age", "country", "home_city", "home_lat", "home_lon", 
            "risk_level", "account_open_date", "avg_monthly_spend"
        )
        # Rename overlapping columns to avoid ambiguous reference if any (e.g. event_timestamp)
        # customer_profile has: age, country, home_city, home_lat, home_lon, risk_level, account_open_date, avg_monthly_spend
        df_gold = df_gold.join(df_cust, on="customer_id", how="left")
        
    df_gold.write.mode("overwrite").parquet(f"{gold_path}/features")
    logger.info("Gold layer build completed.")
    spark.stop()

if __name__ == "__main__":
    run_build_gold()
