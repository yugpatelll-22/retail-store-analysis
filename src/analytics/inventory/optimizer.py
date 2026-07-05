import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_reorder_recommendations(
    forecast_df: pd.DataFrame, 
    lead_time_days: int = 14, 
    service_level_z: float = 1.96
) -> pd.DataFrame:
    """
    Calculates optimal reorder quantities using forecasted demand and safety stock.
    
    Args:
        forecast_df (pd.DataFrame): Prophet forecast output containing 'yhat' (predicted daily demand).
        lead_time_days (int): Supplier lead time in days.
        service_level_z (float): Z-score for service level (1.96 = ~97.5% service level).
        
    Returns:
        pd.DataFrame: Recommended reorder quantities per product/aggregate.
    """
    logger.info("Calculating Inventory Optimization recommendations...")
    
    # Calculate average forecasted daily demand and standard deviation (demand variability)
    avg_daily_demand = forecast_df['yhat'].mean()
    std_dev_demand = forecast_df['yhat'].std()
    
    # Safety Stock Formula: Z * σ_demand * sqrt(Lead Time)
    # This buffers against variability, reducing understock
    safety_stock = service_level_z * std_dev_demand * np.sqrt(lead_time_days)
    
    # Reorder Point Formula: (Average Daily Demand * Lead Time) + Safety Stock
    reorder_point = (avg_daily_demand * lead_time_days) + safety_stock
    
    logger.info(f"Inventory Metrics Computed: ")
    logger.info(f"-> Avg Daily Demand: {avg_daily_demand:.2f} units")
    logger.info(f"-> Safety Stock Level: {safety_stock:.2f} units")
    logger.info(f"-> Reorder Point: {reorder_point:.2f} units")
    
    # Create a summary dataframe for export
    recommendations = pd.DataFrame({
        'Metric': ['Avg_Daily_Demand', 'Safety_Stock', 'Reorder_Point'],
        'Value': [avg_daily_demand, safety_stock, reorder_point]
    })
    
    return recommendations