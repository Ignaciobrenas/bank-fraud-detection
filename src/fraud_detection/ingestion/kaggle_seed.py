import os

def download_paysim():
    """
    Downloads the PaySim dataset from Kaggle for testing with millions of records.
    Requires kaggle CLI installed and configured (~/.kaggle/kaggle.json).
    """
    print("This script will download the ealaxi/paysim1 dataset from Kaggle.")
    print("It contains 6.3 million real-like mobile money transactions.")
    
    # os.system("pip install kaggle")
    # os.system("kaggle datasets download -d ealaxi/paysim1 -p data/raw/ --unzip")
    
    print("\nTo use this data in the pipeline, map the PaySim schema to our Bronze schema:")
    print("PaySim: step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud")
    print("Bronze expected: transaction_id, customer_id, amount, event_timestamp, is_fraud, etc.")

if __name__ == "__main__":
    download_paysim()
