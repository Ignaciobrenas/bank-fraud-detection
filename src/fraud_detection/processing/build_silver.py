import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, abs
from src.fraud_detection.config import CONFIG, logger

def run_build_silver():
    logger.info("Starting Silver layer processing...")
    spark = SparkSession.builder \
        .appName("BankFraud_BuildSilver") \
        .master("local[*]") \
        .getOrCreate()
        
    bronze_path = CONFIG["paths"]["bronze"]
    silver_path = CONFIG["paths"]["silver"]
    
    # 1. Clean Customers
    if os.path.exists(f"{bronze_path}/customer_profile"):
        logger.info("Cleaning customer profiles...")
        df_cust = spark.read.parquet(f"{bronze_path}/customer_profile")
        df_cust = df_cust.dropDuplicates(["customer_id"])
        df_cust.write.mode("overwrite").parquet(f"{silver_path}/customer_profile")
    
    # 2. Clean Devices
    if os.path.exists(f"{bronze_path}/device_data"):
        logger.info("Cleaning device data...")
        df_dev = spark.read.parquet(f"{bronze_path}/device_data")
        df_dev = df_dev.dropDuplicates(["device_id"])
        df_dev.write.mode("overwrite").parquet(f"{silver_path}/device_data")
    
    # 3. Clean Transactions
    logger.info("Cleaning transactions...")
    df_all_tx = None
    if os.path.exists(f"{bronze_path}/transaction_history"):
        df_hist = spark.read.parquet(f"{bronze_path}/transaction_history")
        df_all_tx = df_hist
        
    if os.path.exists(f"{bronze_path}/transactions"):
        df_tx = spark.read.parquet(f"{bronze_path}/transactions")
        if df_all_tx is not None:
            df_all_tx = df_all_tx.unionByName(df_tx, allowMissingColumns=True)
        else:
            df_all_tx = df_tx
            
    if df_all_tx is not None:
        df_all_tx = df_all_tx.dropDuplicates(["transaction_id"])
        df_all_tx = df_all_tx.withColumn("amount", abs(col("amount")))
        df_all_tx = df_all_tx.na.drop(subset=["customer_id", "amount", "event_timestamp"])
        
        # Run Data Quality Checks
        from src.fraud_detection.processing.quality_checks import run_all_checks
        if not run_all_checks(df_all_tx):
            logger.warning("Data quality checks failed for Silver transactions!")
        else:
            logger.info("All data quality checks passed for Silver transactions.")
            
        df_all_tx.write.mode("overwrite").parquet(f"{silver_path}/transactions")
    
    logger.info("Silver layer build completed.")
    spark.stop()

if __name__ == "__main__":
    run_build_silver()
