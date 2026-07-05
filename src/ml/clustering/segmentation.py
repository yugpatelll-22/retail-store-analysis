import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def scale_rfm_data(rfm_df: pd.DataFrame):
    """Scales the RFM data to prepare it for K-Means clustering."""
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_df)
    return rfm_scaled, scaler

def perform_kmeans_clustering(rfm_df: pd.DataFrame, n_clusters: int = 4) -> pd.DataFrame:
    """
    Applies K-Means clustering to the RFM data to create customer segments.
    
    Args:
        rfm_df (pd.DataFrame): RFM table.
        n_clusters (int): Number of segments to create (target is 6-8 based on requirements [1]).
        
    Returns:
        pd.DataFrame: RFM table with an added 'Segment' column.
    """
    logger.info(f"Performing K-Means clustering with {n_clusters} clusters...")
    
    rfm_scaled, scaler = scale_rfm_data(rfm_df)
    
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled)
    
    rfm_df['Segment'] = kmeans.labels_
    
    logger.info(f"Clustering complete. Identified segments: {rfm_df['Segment'].unique()}")
    return rfm_df