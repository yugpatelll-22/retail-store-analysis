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
# PAGE CONFIGURATION & INITIALIZATION
# =====================================================

st.set_page_config(
    page_title="Customer Analytics | RetailPulse AI",
    layout="wide"
)

load_theme()
sidebar()

# =====================================================
# DATA LOADING & FILTERING
# =====================================================

retail, customers, forecast, inventory = load_data()

# Apply global filters to transaction data
retail = global_filters(retail)

# Sync segmented customers with the filtered retail data
valid_customers = retail["Customer ID"].dropna().unique()
filtered_customers = customers[customers["Customer ID"].isin(valid_customers)]

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class='page-title'>👥 Customer Intelligence & RFM Analytics</div>
<div class='subtitle'>Analyze customer behavior, segmentation, lifetime value, and retention cohorts</div>
""", unsafe_allow_html=True)

st.divider()

# =====================================================
# CUSTOMER KPI METRICS
# =====================================================

st.subheader("📈 Customer Base Overview")

total_customers = retail["Customer ID"].nunique()
total_revenue = retail["Revenue"].sum()
clv = total_revenue / total_customers if total_customers > 0 else 0

# Calculate Repeat Purchase Rate
orders_per_customer = retail.groupby("Customer ID")["Invoice"].nunique()
repeat_customers = (orders_per_customer > 1).sum()
repeat_rate = (repeat_customers / total_customers * 100) if total_customers > 0 else 0

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("Total Unique Customers", f"{total_customers:,}")
kpi2.metric("Repeat Customers", f"{repeat_customers:,}")
kpi3.metric("Repeat Purchase Rate", f"{repeat_rate:.1f}%")
kpi4.metric("Avg Customer Lifetime Value", f"£{clv:,.2f}")

st.divider()

# =====================================================
# RFM SEGMENTATION ANALYSIS
# =====================================================

st.subheader("🎯 RFM Customer Segmentation (Recency, Frequency, Monetary)")

if not filtered_customers.empty:
    seg_col1, seg_col2 = st.columns([1, 1.5])
    
    # 1. Segment Distribution Treemap
    with seg_col1:
        segment_counts = filtered_customers.groupby("Segment").size().reset_index(name="Count")
        fig_tree = px.treemap(
            segment_counts, 
            path=["Segment"], 
            values="Count",
            color="Count",
            color_continuous_scale="Purples",
            title="Customer Segment Distribution"
        )
        fig_tree.update_layout(
            template="plotly_dark", 
            paper_bgcolor="#0B1120", 
            plot_bgcolor="#0B1120",
            height=450,
            margin=dict(t=40, l=10, r=10, b=10)
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    # 2. RFM Scatter/Bubble Chart
    with seg_col2:
        fig_scatter = px.scatter(
            filtered_customers, 
            x="Recency", 
            y="Frequency", 
            size="Monetary", 
            color="Segment",
            hover_name="Customer ID",
            size_max=45,
            title="RFM Value Matrix (Bubble Size = Monetary Value)",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_scatter.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0B1120",
            plot_bgcolor="#0B1120",
            height=450,
            xaxis_title="Recency (Days Since Last Purchase)",
            yaxis_title="Frequency (Number of Purchases)"
        )
        # Reverse X-axis so lower recency (better) is on the right
        fig_scatter.update_xaxes(autorange="reversed")
        st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning("Customer segmentation data is unavailable for the selected filters.")

st.divider()

# =====================================================
# COHORT ANALYSIS & RETENTION
# =====================================================

st.subheader("🗓️ Customer Cohort Analysis & Retention Heatmap")

try:
    # Prepare data for cohort analysis
    cohort_data = retail[['Customer ID', 'InvoiceDate']].dropna().copy()
    cohort_data['OrderMonth'] = cohort_data['InvoiceDate'].dt.to_period('M')
    cohort_data['CohortMonth'] = cohort_data.groupby('Customer ID')['InvoiceDate'].transform('min').dt.to_period('M')
    
    # Group by CohortMonth and OrderMonth
    cohort_group = cohort_data.groupby(['CohortMonth', 'OrderMonth']).agg(n_customers=('Customer ID', 'nunique')).reset_index()
    
    # Calculate period distance
    cohort_group['PeriodNumber'] = (cohort_group.OrderMonth - cohort_group.CohortMonth).apply(lambda x: x.n)
    
    # Pivot into matrix
    cohort_pivot = cohort_group.pivot_table(index='CohortMonth', columns='PeriodNumber', values='n_customers')
    cohort_size = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0)
    
    # Format indices for display
    retention_matrix.index = retention_matrix.index.astype(str)
    
    # Plotly Heatmap
    fig_cohort = go.Figure(data=go.Heatmap(
        z=retention_matrix.values,
        x=retention_matrix.columns,
        y=retention_matrix.index,
        colorscale='Blues',
        text=np.round(retention_matrix.values * 100, 1),
        texttemplate="%{text}%",
        showscale=True
    ))
    
    fig_cohort.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B1120",
        plot_bgcolor="#0B1120",
        height=500,
        xaxis_title="Months Since First Purchase (Period)",
        yaxis_title="Cohort Acquisition Month",
        yaxis_autorange="reversed"
    )
    
    st.plotly_chart(fig_cohort, use_container_width=True)

except Exception as e:
    st.info("Insufficient data points across multiple months to generate Cohort Retention Heatmap.")

st.divider()

# =====================================================
# VIP CUSTOMER INTELLIGENCE
# =====================================================

st.subheader("👑 VIP Customer Ledger")

vip_col1, vip_col2 = st.columns([3, 1])

with vip_col1:
    # Filter for top segments (assuming segments like 'Champions' or 'Loyal' exist in the CSV)
    # For robust functionality, we'll sort by Monetary regardless of segment naming
    top_customers = filtered_customers.sort_values(by="Monetary", ascending=False).head(50)
    
    st.dataframe(
        top_customers.style.format({
            "Recency": "{:.0f} Days",
            "Frequency": "{:.0f} Orders",
            "Monetary": "£{:,.2f}"
        }).background_gradient(subset=['Monetary'], cmap='Blues'),
        use_container_width=True,
        height=350
    )

with vip_col2:
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 24px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1); height: 350px;">
        <h4 style="color: #3B82F6; margin-top: 0;">Export VIP Data</h4>
        <p style="color: #94A3B8; font-size: 0.9em;">Download this segmented ledger to import directly into your CRM or email marketing platform for targeted VIP campaigns.</p>
    </div>
    """, unsafe_allow_html=True)
    
    csv_vip = top_customers.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download VIP Customer CSV",
        data=csv_vip,
        file_name="retail_pulse_vip_customers.csv",
        mime="text/csv",
        use_container_width=True
    )