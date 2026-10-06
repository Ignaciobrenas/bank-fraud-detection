from pyspark.sql import DataFrame
from pyspark.sql.functions import col

def check_no_nulls(df: DataFrame, columns: list) -> bool:
    """Returns True if no nulls exist in the specified columns."""
    for c in columns:
        if df.filter(col(c).isNull()).count() > 0:
            print(f"Quality Check Failed: Null values found in column '{c}'")
            return False
    return True

def check_positive_amount(df: DataFrame, amount_col: str = "amount") -> bool:
    """Returns True if all amounts are >= 0."""
    if df.filter(col(amount_col) < 0).count() > 0:
        print(f"Quality Check Failed: Negative amounts found in column '{amount_col}'")
        return False
    return True

def run_all_checks(df_tx: DataFrame) -> bool:
    """Run a suite of quality checks on transactions."""
    passed = True
    if not check_no_nulls(df_tx, ["transaction_id", "customer_id", "amount", "event_timestamp"]):
        passed = False
    if not check_positive_amount(df_tx):
        passed = False
    return passed
