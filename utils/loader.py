import pandas as pd
import streamlit as st


@st.cache_data
def load_data():

    retail = pd.read_csv(
        "data/processed_retail_data.csv",
        parse_dates=["InvoiceDate"]
    )

    customers = pd.read_csv(
        "data/segmented_customers.csv"
    )

    forecast = pd.read_csv(
        "data/prophet_30_day_forecast.csv"
    )

    inventory = pd.read_csv(
        "data/inventory_recommendations.csv"
    )

    return retail,customers,forecast,inventory