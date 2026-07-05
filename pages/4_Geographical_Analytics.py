import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.loader import load_data
from components.filters import global_filters
from components.theme import load_theme
from components.sidebar import sidebar

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Geographical Analytics | RetailPulse AI",
    layout="wide"
)

load_theme()
sidebar()

# =====================================================
# LOAD & FILTER DATA
# =====================================================

retail, customers, forecast, inventory = load_data()
retail = global_filters(retail)

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class='page-title'>🌍 Geographical Analytics & Market Expansion</div>
<div class='subtitle'>Analyze global footprint, regional revenue distribution, and country-level performance</div>
""", unsafe_allow_html=True)

st.divider()

# =====================================================
# GEOGRAPHICAL KPIs
# =====================================================

st.subheader("📍 Global Footprint Overview")

# Calculate Geo Metrics
total_countries = retail["Country"].nunique()
domestic_revenue = retail[retail["Country"] == "United Kingdom"]["Revenue"].sum() if "United Kingdom" in retail["Country"].values else 0
total_revenue = retail["Revenue"].sum()
intl_revenue = total_revenue - domestic_revenue
intl_percentage = (intl_revenue / total_revenue * 100) if total_revenue > 0 else 0

top_intl_market = retail[retail["Country"] != "United Kingdom"].groupby("Country")["Revenue"].sum().idxmax() if total_countries > 1 else "N/A"

geo_kpi1, geo_kpi2, geo_kpi3, geo_kpi4 = st.columns(4)

geo_kpi1.metric("Active Territories", f"{total_countries}")
geo_kpi2.metric("International Revenue", f"£{intl_revenue:,.0f}")
geo_kpi3.metric("Intl. Revenue Share", f"{intl_percentage:.1f}%")
geo_kpi4.metric("Top Intl. Market", top_intl_market)

st.divider()

# =====================================================
# GLOBAL CHOROPLETH MAP
# =====================================================

st.subheader("🗺️ Global Revenue Distribution Map")

# Aggregate data by country
country_agg = retail.groupby("Country").agg(
    Revenue=("Revenue", "sum"),
    Orders=("Invoice", "nunique"),
    Customers=("Customer ID", "nunique"),
    Units_Sold=("Quantity", "sum")
).reset_index()

fig_map = px.choropleth(
    country_agg,
    locations="Country",
    locationmode="country names",
    color="Revenue",
    hover_name="Country",
    hover_data={
        "Revenue": ":,.2f",
        "Orders": True,
        "Customers": True,
        "Units_Sold": True
    },
    color_continuous_scale="Blues",
    title="Revenue Heatmap by Country"
)

fig_map.update_layout(
    template="plotly_dark",
    paper_bgcolor="#0B1120",
    geo_bgcolor="#0B1120",
    height=600,
    margin=dict(l=0, r=0, t=40, b=0),
    coloraxis_colorbar=dict(title="Revenue (£)")
)
fig_map.update_geos(
    showcoastlines=True, coastlinecolor="rgba(255, 255, 255, 0.1)",
    showland=True, landcolor="#1E293B",
    showocean=True, oceancolor="#0B1120",
    projection_type="natural earth"
)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

# =====================================================
# REGIONAL COMPARISON CHARTS
# =====================================================

st.subheader("📊 Market Performance Comparisons")

col_comp1, col_comp2 = st.columns(2)

with col_comp1:
    # Top 10 Countries by Orders
    top_orders = country_agg.sort_values("Orders", ascending=False).head(10)
    fig_orders = px.bar(
        top_orders, 
        x="Orders", 
        y="Country", 
        orientation="h",
        color="Orders",
        color_continuous_scale="Teal",
        title="Top 10 Markets by Order Volume"
    )
    fig_orders.update_layout(
        template="plotly_dark", paper_bgcolor="#0B1120", plot_bgcolor="#0B1120",
        height=400, coloraxis_showscale=False, yaxis={'categoryorder':'total ascending'},
        xaxis_title="Total Orders", yaxis_title=""
    )
    st.plotly_chart(fig_orders, use_container_width=True)

with col_comp2:
    # Average Order Value by Country (Top 10 by Revenue)
    top_rev_countries = country_agg.sort_values("Revenue", ascending=False).head(10).copy()
    top_rev_countries["AOV"] = top_rev_countries["Revenue"] / top_rev_countries["Orders"]
    top_rev_countries = top_rev_countries.sort_values("AOV", ascending=True)
    
    fig_aov = px.bar(
        top_rev_countries,
        x="AOV",
        y="Country",
        orientation="h",
        color="AOV",
        color_continuous_scale="Purples",
        title="Average Order Value (£) in Top Markets"
    )
    fig_aov.update_layout(
        template="plotly_dark", paper_bgcolor="#0B1120", plot_bgcolor="#0B1120",
        height=400, coloraxis_showscale=False,
        xaxis_title="Average Order Value (£)", yaxis_title=""
    )
    st.plotly_chart(fig_aov, use_container_width=True)

st.divider()

# =====================================================
# INTERACTIVE MARKET LEDGER
# =====================================================

st.subheader("📑 Interactive Market Performance Ledger")

# Format the dataframe for display
display_df = country_agg.copy()
display_df["AOV"] = display_df["Revenue"] / display_df["Orders"]
display_df = display_df.sort_values("Revenue", ascending=False)

# Render as an interactive dataframe
st.dataframe(
    display_df.style.format({
        "Revenue": "£{:,.2f}",
        "Orders": "{:,}",
        "Customers": "{:,}",
        "Units_Sold": "{:,}",
        "AOV": "£{:,.2f}"
    }).background_gradient(subset=['Revenue'], cmap='Blues'),
    use_container_width=True,
    height=400
)

# Export Data
st.markdown("<br>", unsafe_allow_html=True)
csv_geo = country_agg.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Complete Geographical Ledger (CSV)",
    data=csv_geo,
    file_name="retail_pulse_geographical_metrics.csv",
    mime="text/csv"
)