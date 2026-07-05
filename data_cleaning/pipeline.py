import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import custom modules
from .loader import load_data
from .cleaner import run_cleaning
from src.etl.feature_engineering.feature_engineer import run_feature_engineering
from src.analytics.statistics.eda import run_eda
from src.etl.feature_engineering.rfm_engineer import calculate_rfm
from src.ml.clustering.segmentation import perform_kmeans_clustering
from src.analytics.forecasting.prophet_model import train_prophet_model, generate_prophet_forecast
from src.etl.feature_engineering.rfm_engineer import calculate_rfm
from src.ml.clustering.segmentation import perform_kmeans_clustering
from src.etl.feature_engineering.churn_labeler import label_churn_rfm    
from src.ml.classification.churn_model import train_churn_model         
from src.analytics.inventory.optimizer import calculate_reorder_recommendations

def run_etl_pipeline(input_path: str, processed_output_path: str, figures_output_dir: str):
    """
    Orchestrates the extraction, cleaning, transformation, and EDA of retail data.
    """
    logger.info("Executing RetailPulse End-to-End ETL & EDA Pipeline...")
    
    # 1. Extract
    df_raw = load_data(input_path)
    logger.info("Data extracted successfully.")
    # 2. Clean (F-01)
    df_clean = run_cleaning(df_raw)
    
    # 3. Feature Engineering
    df_processed = run_feature_engineering(df_clean)
    
    # 4. Save Processed Data
    os.makedirs(os.path.dirname(processed_output_path), exist_ok=True)
    df_processed.to_csv(processed_output_path, index=False)
    logger.info(f"Processed data saved to {processed_output_path}")
    
    # 5. Run EDA
     
    # 5. Run EDA
    run_eda(df_processed, figures_output_dir)
    
    # 6. Customer Segmentation (F-02)
    logger.info("Starting Customer Segmentation...")
    rfm_table = calculate_rfm(df_processed)
    segmented_customers = perform_kmeans_clustering(rfm_table, n_clusters=6)
    
    # Save the segmented customer data
    segmented_customers.to_csv("data/segmented_customers.csv")
    logger.info("Customer Segmentation complete. Saved to data/segmented_customers.csv")
    
    logger.info("Pipeline execution finished successfully!")  
    # 5. Run EDA
    run_eda(df_processed, figures_output_dir)
    
    # 6. Customer Segmentation (F-02)
    logger.info("Starting Customer Segmentation...")
    rfm_table = calculate_rfm(df_processed)
    segmented_customers = perform_kmeans_clustering(rfm_table, n_clusters=6)
    
    # 7. Demand Forecasting (F-03)
    logger.info("Starting Demand Forecasting...")
    prophet_model = train_prophet_model(df_processed)
    prophet_forecast = generate_prophet_forecast(prophet_model, periods=30)
    
    # 8. Inventory Optimization (F-05)
    logger.info("Starting Inventory Optimization...")
    inventory_recommendations = calculate_reorder_recommendations(prophet_forecast, lead_time_days=14)
    
    # Save the inventory recommendations
    inventory_recommendations.to_csv("data/inventory_recommendations.csv", index=False)
    logger.info("Inventory Optimization complete. Saved to data/inventory_recommendations.csv")
    
    logger.info("Pipeline execution finished successfully!")

if __name__ == "__main__":
    # Define paths
    INPUT_FILE = "C:\\Users\\yugpa\\OneDrive\\Computer\\Desktop (1)\\retail\\data_cleaning\\data\\online_retail_II.xlsx"
    PROCESSED_OUTPUT_FILE = "data/processed_retail_data.csv"
    FIGURES_DIR = "reports/figures"
    
    run_etl_pipeline(
        input_path=INPUT_FILE, 
        processed_output_path=PROCESSED_OUTPUT_FILE,
        figures_output_dir=FIGURES_DIR
    )