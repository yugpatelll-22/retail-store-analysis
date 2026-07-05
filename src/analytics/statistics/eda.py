import pandas as pd
import plotly.express as px
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def plot_monthly_revenue(df: pd.DataFrame, output_dir: str):
    """Plots monthly revenue trend to identify seasonality for demand forecasting."""
    logger.info("Generating Monthly Revenue Trend plot...")
    
    # Aggregate data by Year and Month
    monthly_data = df.groupby(['Year', 'Month'])['Revenue'].sum().reset_index()
    monthly_data['Date'] = pd.to_datetime(monthly_data['Year'].astype(str) + '-' + monthly_data['Month'].astype(str) + '-01')
    
    fig = px.line(
        monthly_data, 
        x='Date', 
        y='Revenue', 
        title='Monthly Revenue Trend (Identifying Seasonality)',
        labels={'Revenue': 'Total Revenue (£)', 'Date': 'Month'},
        template='plotly_dark'
    )
    
    fig.update_traces(line_color='#00D4FF', line_width=3)
    fig.update_layout(title_x=0.5)
    
    save_path = os.path.join(output_dir, 'monthly_revenue_trend.png')
    fig.write_image(save_path)
    logger.info(f"Saved Monthly Revenue Trend to {save_path}")

def plot_top_products(df: pd.DataFrame, output_dir: str, top_n=10):
    """Plots top N products by revenue to identify key inventory drivers."""
    logger.info(f"Generating Top {top_n} Products by Revenue plot...")
    
    product_rev = df.groupby('Description')['Revenue'].sum().nlargest(top_n).reset_index()
    
    fig = px.bar(
        product_rev, 
        x='Revenue', 
        y='Description', 
        orientation='h', 
        title=f'Top {top_n} Products by Revenue',
        labels={'Revenue': 'Total Revenue (£)', 'Description': 'Product'},
        template='plotly_dark'
    )
    
    fig.update_traces(marker_color='#FF6B6B')
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, title_x=0.5)
    
    save_path = os.path.join(output_dir, 'top_products_revenue.png')
    fig.write_image(save_path)
    logger.info(f"Saved Top Products plot to {save_path}")

def plot_country_revenue(df: pd.DataFrame, output_dir: str, top_n=10):
    """Plots revenue by country to assist with geographic inventory optimization."""
    logger.info(f"Generating Top {top_n} Countries by Revenue plot...")
    
    country_rev = df.groupby('Country')['Revenue'].sum().nlargest(top_n).reset_index()
    
    fig = px.pie(
        country_rev, 
        values='Revenue', 
        names='Country', 
        title=f'Revenue Distribution by Top {top_n} Countries',
        hole=0.4, # Creates a donut chart for better aesthetics
        template='plotly_dark'
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(title_x=0.5)
    
    save_path = os.path.join(output_dir, 'country_revenue_distribution.png')
    fig.write_image(save_path)
    logger.info(f"Saved Country Revenue plot to {save_path}")

def run_eda(df: pd.DataFrame, output_dir: str):
    """Orchestrates EDA visualizations."""
    os.makedirs(output_dir, exist_ok=True)
    logger.info("Starting Exploratory Data Analysis...")
    plot_monthly_revenue(df, output_dir)
    plot_top_products(df, output_dir)
    plot_country_revenue(df, output_dir)
    logger.info("EDA complete. Visualizations saved.")