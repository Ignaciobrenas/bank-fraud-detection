import yaml
import logging
from pathlib import Path

def load_config(config_path="config/settings.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

CONFIG = load_config()

# Centralized Logging Setup
def get_logger(name="BankFraud"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fmt = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(fmt)
        logger.addHandler(ch)
        
        # File handler
        Path("logs").mkdir(exist_ok=True)
        fh = logging.FileHandler("logs/pipeline.log")
        fh.setFormatter(fmt)
        logger.addHandler(fh)
        
    return logger

logger = get_logger()
