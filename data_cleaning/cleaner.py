import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handles missing values strategically."""
    initial_rows = len(df)
    
    # Customer ID is critical for RFM and Segmentation (F-02). 
    # We cannot impute it blindly, so we drop rows where Customer ID is missing.
    df = df.dropna(subset=['Customer ID'])
    
    # Drop rows where Description is missing (minimal data loss)
    df = df.dropna(subset=['Description'])
    
    logger.info(f"Removed {initial_rows - len(df):,} rows with missing critical values (Customer ID, Description).")
    return df

def clean_invalid_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Handles cancelled orders, negative quantities, and zero prices."""
    # In retail datasets, 'C' prefix indicates cancellations. 
    # For demand forecasting, we separate these, but for general analytics, we drop them.
    cancellations = df[df['Invoice'].astype(str).str.startswith('C')]
    logger.info(f"Identified {len(cancellations):,} cancellation transactions.")
    
    # Filter out cancellations
    df = df[~df['Invoice'].astype(str).str.startswith('C')]
    
    # Quantity must be positive for valid sales demand
    df = df[df['Quantity'] > 0]
    
    # Price must be positive
    df = df[df['Price'] > 0]
    
    logger.info(f"Filtered out cancellations, negative quantities, and zero prices. Rows remaining: {len(df):,}")
    return df

def clean_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Converts columns to appropriate data types for downstream ML."""
    df['Invoice'] = df['Invoice'].astype(str)
    df['StockCode'] = df['StockCode'].astype(str)
    df['Description'] = df['Description'].str.strip().str.upper() # Standardize text
    df['Customer ID'] = df['Customer ID'].astype(int).astype(str) # Convert from float to string
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['Country'] = df['Country'].str.strip().str.upper()
    
    logger.info("Data types successfully converted and text standardized.")
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Removes exact duplicate transactions."""
    initial_rows = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {initial_rows - len(df):,} exact duplicate rows.")
    return df

def run_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """Master function to run all cleaning steps."""
    logger.info("Starting data cleaning pipeline...")
    df = clean_missing_values(df)
    df = clean_invalid_transactions(df)
    df = remove_duplicates(df)
    df = clean_data_types(df)
    logger.info(f"Cleaning complete. Final dataset size: {len(df):,} records.")
    return df