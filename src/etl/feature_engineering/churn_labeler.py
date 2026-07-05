import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def label_churn_rfm(rfm_df: pd.DataFrame, churn_threshold_days: int = 90) -> pd.DataFrame:
    """
    Labels customers as Churn (1) or Active (0) based on a recency threshold.
    
    Args:
        rfm_df (pd.DataFrame): RFM table with 'Recency' column.
        churn_threshold_days (int): Number of days beyond which a customer is considered churned.
        
    Returns:
        pd.DataFrame: RFM table with an added 'Churn' column.
    """
    logger.info(f"Labeling churn with threshold of {churn_threshold_days} days...")
    
    rfm_df['Churn'] = np.where(rfm_df['Recency'] > churn_threshold_days, 1, 0)
    
    churn_rate = rfm_df['Churn'].mean() * 100
    logger.info(f"Churn labeling complete. Overall churn rate: {churn_rate:.2f}%")
    return rfm_df