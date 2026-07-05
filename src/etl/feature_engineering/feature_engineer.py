import pandas as pd
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_revenue_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates total transaction revenue."""
    df['Revenue'] = df['Quantity'] * df['Price']
    logger.info("Created 'Revenue' feature (Quantity * Price).")
    return df

def create_time_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extracts time-based features from InvoiceDate for seasonality and forecasting."""
    df['Year'] = df['InvoiceDate'].dt.year
    df['Month'] = df['InvoiceDate'].dt.month
    df['Day'] = df['InvoiceDate'].dt.day
    df['DayOfWeek'] = df['InvoiceDate'].dt.dayofweek  # Monday=0, Sunday=6
    df['Hour'] = df['InvoiceDate'].dt.hour
    
    # Boolean flag for weekend (Sat=5, Sun=6)
    df['IsWeekend'] = df['DayOfWeek'].isin([5, 6]).astype(int)
    
    logger.info("Created time-based features (Year, Month, Day, DayOfWeek, Hour, IsWeekend).")
    return df

def run_feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """Orchestrates the feature engineering process."""
    logger.info("Starting Feature Engineering pipeline...")
    df = create_revenue_feature(df)
    df = create_time_features(df)
    logger.info("Feature Engineering complete.")
    return df