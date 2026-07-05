import pandas as pd
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data(file_path: str) -> pd.DataFrame:
    """
    Ingests the Online Retail II dataset from the Excel file.
    Handles the dual sheets ('Year 2009-2010' and 'Year 2010-2011') 
    and combines them into a single DataFrame.
    
    Args:
        file_path (str): Path to the online_retail_II.xlsx file.
        
    Returns:
        pd.DataFrame: Combined raw dataset.
    """
    if not os.path.exists(file_path):
        logger.error(f"Data file not found at {file_path}")
        raise FileNotFoundError(f"Please place the dataset in {file_path}")
        
    logger.info(f"Starting data ingestion from {file_path}")
    
    try:
        # Read both sheets simultaneously
        df1 = pd.read_excel(file_path, sheet_name="Year 2009-2010")
        df2 = pd.read_excel(file_path, sheet_name="Year 2010-2011")
        
        # Add traceability for the data source
        df1['Batch_Year'] = "2009-2010"
        df2['Batch_Year'] = "2010-2011"
        
        # Combine into a single dataframe
        df = pd.concat([df1, df2], ignore_index=True)
        logger.info(f"Successfully ingested {len(df):,} total records.")
        
        return df
        
    except Exception as e:
        logger.error(f"Error during data ingestion: {e}")
        raise