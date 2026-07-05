import pandas as pd
from prophet import Prophet
import logging
from typing import cast, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def train_prophet_model(df: pd.DataFrame) -> Prophet:
    """
    Trains a baseline Prophet model on daily revenue data.
    
    Args:
        df (pd.DataFrame): Processed DataFrame with 'InvoiceDate' and 'Revenue'.
        
    Returns:
        Prophet: Fitted Prophet model.
    """
    logger.info("Training baseline Prophet model for demand forecasting...")
    
    # Prophet requires columns to be named 'ds' (datestamp) and 'y' (target)
    daily_data = df.groupby(pd.Grouper(key='InvoiceDate', freq='D'))['Revenue'].sum().reset_index()
    daily_data.rename(columns={'InvoiceDate': 'ds', 'Revenue': 'y'}, inplace=True)
    
    model = Prophet(
        yearly_seasonality=cast(Any, True),
        weekly_seasonality=cast(Any, True),
        daily_seasonality=cast(Any, False),
        seasonality_mode='multiplicative'
    )
    
    model.fit(daily_data)
    logger.info("Prophet model training complete.")
    return model

def generate_prophet_forecast(model: Prophet, periods: int = 30) -> pd.DataFrame:
    """
    Generates future predictions using the trained Prophet model.
    
    Args:
        model (Prophet): Trained Prophet model.
        periods (int): Number of days to predict ahead.
        
    Returns:
        pd.DataFrame: Forecasted data.
    """
    logger.info(f"Generating {periods}-day forecast with Prophet...")
    future = model.make_future_dataframe(periods=periods)
    forecast = model.predict(future)
    return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)