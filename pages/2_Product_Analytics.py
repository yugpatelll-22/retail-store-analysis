import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.loader import load_data
from components.filters import global_filters
from components.theme import load_theme
from components.sidebar import sidebar

# =====================================================
# PAGE SETUP & STYLING
# =====================================================

st.set_page_config(
    page_title="Product Analytics | RetailPulse AI",
    layout="wide"
)

load_theme()
sidebar()

# =====================================================
# LOAD & FILTER DATASET
# =====================================================

retail, customers, forecast, inventory = load_data()
retail = global_filters(retail)

st.markdown("""
<div class='page-title'>📦 Product Intelligence & Inventory Analytics</div>
<div class='subtitle'>Deep-dive performance matrices, velocity metrics, and demand forecasting</div>
""", unsafe_allow_html=True)

st.divider()

# =====================================================
# ADVANCED INTERACTIVE PRODUCT DEEP-DIVE SEARCH
# =====================================================

st.subheader("🔍 Interactive Product Search Matrix")
print(retail.columns.tolist())
all_products = sorted(retail["Description"].unique())
selected_product = st.selectbox("Select a target product for deep optimization analysis:", all_products)

prod_df = retail[retail["Description"] == selected_product]

if not prod_df.empty:
    p_rev = prod_df["Revenue"].sum()
    p_qty = prod_df["Quantity"].sum()
    p_orders = prod_df["Invoice"].nunique()
    p_avg_price = prod_df["Price"].mean()
    
    sc1, sc2, sc3, sc4 = st.columns(4)
    sc1.metric("Product Revenue", f"£{p_rev:,.2f}")
    sc2.metric("Units Sold", f"{p_qty:,}")
    sc3.metric("Unique Orders", f"{p_orders:,}")
    sc4.metric("Average Unit Price", f"£{p_avg_price:,.2f}")
    
    # Velocity Chart (Daily Sales Run Rate)
    daily_velocity = prod_df.groupby("InvoiceDate")["Quantity"].sum().reset_index()
    fig_vel = px.line(
        daily_velocity, x="InvoiceDate", y="Quantity", 
        title=f"Sales Velocity Trendline: {selected_product}",
        color_discrete_sequence=["#10B981"]
    )
    fig_vel.update_layout(template="plotly_dark", paper_bgcolor="#0B1120", plot_bgcolor="#0B1120", height=300)
    st.plotly_chart(fig_vel, use_container_width=True)
else:
    st.warning("No transactional data matching the criteria found for this specific item.")

st.divider()

# =====================================================
# ABC & PARETO CLASSIFICATION
# =====================================================

st.subheader("📊 Product Inventory ABC & Pareto Classification")

abc_df = retail.groupby("Description")["Revenue"].sum().reset_index()
abc_df = abc_df.sort_values(by="Revenue", ascending=False).reset_index(drop=True)
abc_df["CumRevenue"] = abc_df["Revenue"].cumsum()
total_revenue = abc_df["Revenue"].sum()
abc_df["CumPercentage"] = (abc_df["CumRevenue"] / total_revenue) * 100

def classify_abc(percentage):
    if percentage <= 80:
        return 'A (High Value)'
    elif percentage <= 95:
        return 'B (Medium Value)'
    else:
        return 'C (Low Value)'

abc_df["Class"] = abc_df["CumPercentage"].apply(classify_abc)
st.write("ABC DF Columns:", abc_df.columns.tolist())
abc_summary = abc_df.groupby("Class").agg(
    Product_Count=("Description", "count"),
    Total_Revenue=("Revenue", "sum")
).reset_index()

abc_c1, abc_c2 = st.columns([1, 2])

with abc_c1:
    st.dataframe(abc_summary.style.format({"Total_Revenue": "£{:,.2f}"}), use_container_width=True)
    fig_pie = px.pie(abc_summary, names="Class", values="Product_Count", color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.4)
    fig_pie.update_layout(template="plotly_dark", paper_bgcolor="#0B1120", plot_bgcolor="#0B1120", height=280, showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

with abc_c2:
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(x=abc_df.index[:30], y=abc_df["Revenue"][:30], name="Revenue", marker_color="#3B82F6"))
    fig_pareto.add_trace(go.Scatter(x=abc_df.index[:30], y=abc_df["CumPercentage"][:30], name="Cumulative %", yaxis="y2", line=dict(color="#EF4444", width=2)))
    
    fig_pareto.update_layout(
        title="Pareto Principle Analysis (Top 30 Products)",
        template="plotly_dark", paper_bgcolor="#0B1120", plot_bgcolor="#0B1120", height=400,
        yaxis=dict(title="Revenue (£)"),
        yaxis2=dict(title="Cumulative Percent (%)", overlaying="y", side="right", range=[0, 105])
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

st.divider()

# =====================================================
# TREEMAP ANALYSIS & DATA DOWNLOAD
# =====================================================

st.subheader("🌳 Product Hierarchy Treemap (Volume vs Revenue)")

top_tree = abc_df.head(50)
fig_tree = px.treemap(
    top_tree, path=["Class", "Description"], values="Revenue",
    color="Revenue", color_continuous_scale="Blues"
)
fig_tree.update_layout(template="plotly_dark", paper_bgcolor="#0B1120", height=500)
st.plotly_chart(fig_tree, use_container_width=True)

st.subheader("📥 Export Advanced Inventory Classification Data")
csv_abc = abc_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Complete Product ABC Matrix (CSV)",
    data=csv_abc,
    file_name="retail_pulse_abc_inventory_analysis.csv",
    mime="text/csv",
    use_container_width=True
)