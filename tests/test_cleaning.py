import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from src.fraud_detection.processing.quality_checks import check_no_nulls, check_positive_amount

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.appName("TestSpark").master("local[1]").getOrCreate()

def test_check_no_nulls(spark):
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("val", StringType(), True)
    ])
    data_good = [("1", "A"), ("2", "B")]
    data_bad = [("1", "A"), (None, "B")]
    
    df_good = spark.createDataFrame(data_good, schema)
    df_bad = spark.createDataFrame(data_bad, schema)
    
    assert check_no_nulls(df_good, ["id", "val"]) == True
    assert check_no_nulls(df_bad, ["id", "val"]) == False

def test_check_positive_amount(spark):
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("amount", DoubleType(), True)
    ])
    data_good = [("1", 10.5), ("2", 0.0)]
    data_bad = [("1", 10.5), ("2", -5.0)]
    
    df_good = spark.createDataFrame(data_good, schema)
    df_bad = spark.createDataFrame(data_bad, schema)
    
    assert check_positive_amount(df_good) == True
    assert check_positive_amount(df_bad) == False
