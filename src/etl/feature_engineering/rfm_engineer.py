import pandas as pd
import numpy as np
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Recency, Frequency, and Monetary values for each customer.
    
    Args:
        df (pd.DataFrame): Processed retail data with 'Customer ID', 'InvoiceDate', 'Invoice', and 'Revenue'.
        
    Returns:
        pd.DataFrame: Aggregated RFM table per Customer ID.
    """
    logger.info("Calculating RFM metrics...")
    
    # Assume the max date in the dataset is the current date for Recency calculation
    current_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby('Customer ID').agg({
        'InvoiceDate': lambda x: (current_date - x.max()).days,  # Recency
        'Invoice': 'nunique',                                    # Frequency
        'Revenue': 'sum'                                        # Monetary
    })
    
    # Rename columns
    rfm.rename(columns={
        'InvoiceDate': 'Recency',
        'Invoice': 'Frequency',
        'Revenue': 'Monetary'
    }, inplace=True)
    
    logger.info(f"RFM calculation complete. Shape: {rfm.shape}")
    return rfm