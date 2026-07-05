import streamlit as st
import pandas as pd
import plotly.express as px

from utils.loader import load_data
from components.cards import metric_card
from components.filters import global_filters
from components.theme import load_theme
from components.sidebar import sidebar

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide"
)

load_theme()
sidebar()

# =====================================================
# LOAD DATA
# =====================================================

retail, customers, forecast, inventory = load_data()

retail = global_filters(retail)

# =====================================================
# PAGE TITLE
# =====================================================

st.markdown("""
<div class='page-title'>
📊 Executive Dashboard
</div>

<div class='subtitle'>
Complete overview of your retail business
</div>
""", unsafe_allow_html=True)

# =====================================================
# KPI CALCULATIONS
# =====================================================

total_revenue = retail["Revenue"].sum()

total_orders = retail["Invoice"].nunique()

total_customers = retail["Customer ID"].nunique()

countries = retail["Country"].nunique()

average_order = total_revenue / total_orders if total_orders else 0

average_customer = total_revenue / total_customers if total_customers else 0

# =====================================================
# KPI CARDS
# =====================================================

c1,c2,c3 = st.columns(3)

with c1:

    metric_card(
        "💰 Revenue",
        f"£{total_revenue:,.0f}",
        "blue"
    )

with c2:

    metric_card(
        "🛒 Orders",
        f"{total_orders:,}",
        "green"
    )

with c3:

    metric_card(
        "👥 Customers",
        f"{total_customers:,}",
        "purple"
    )

c4,c5,c6 = st.columns(3)

with c4:

    metric_card(
        "🌍 Countries",
        countries,
        "orange"
    )

with c5:

    metric_card(
        "💳 Avg Order Value",
        f"£{average_order:,.2f}",
        "blue"
    )

with c6:

    metric_card(
        "⭐ Revenue / Customer",
        f"£{average_customer:,.2f}",
        "green"
    )

st.divider()

# =====================================================
# MONTHLY REVENUE
# =====================================================

st.subheader("📈 Monthly Revenue Trend")

monthly = (

    retail

    .groupby(

        pd.Grouper(

            key="InvoiceDate",

            freq="ME"

        )

    )["Revenue"]

    .sum()

    .reset_index()

)

fig = px.area(

    monthly,

    x="InvoiceDate",

    y="Revenue",

    markers=True,

    color_discrete_sequence=["#3B82F6"]

)

fig.update_layout(

    template="plotly_dark",

    paper_bgcolor="#0B1120",

    plot_bgcolor="#0B1120",

    height=450,

    xaxis_title="",

    yaxis_title="Revenue (£)",

    hovermode="x unified"

)

st.plotly_chart(

    fig,

    use_container_width=True

)

# =====================================================
# SALES BY MONTH
# =====================================================

st.subheader("📅 Revenue by Month")

month_sales = (

    retail

    .groupby(

        retail["InvoiceDate"].dt.month_name()

    )["Revenue"]

    .sum()

    .reset_index()

)

months = [

"January",

"February",

"March",

"April",

"May",

"June",

"July",

"August",

"September",

"October",

"November",

"December"

]

month_sales["InvoiceDate"] = pd.Categorical(

    month_sales["InvoiceDate"],

    categories=months,

    ordered=True

)

month_sales = month_sales.sort_values(

    "InvoiceDate"

)

fig2 = px.bar(

    month_sales,

    x="InvoiceDate",

    y="Revenue",

    color="Revenue",

    color_continuous_scale="Blues",

    text_auto=True

)

fig2.update_layout(

    template="plotly_dark",

    paper_bgcolor="#0B1120",

    plot_bgcolor="#0B1120",

    height=420,

    xaxis_title="",

    yaxis_title="Revenue (£)"

)

st.plotly_chart(

    fig2,

    use_container_width=True

)

st.divider()
# =====================================================
# GEOGRAPHIC ANALYSIS (WORLD MAP & COUNTRY LEADERBOARD)
# =====================================================

st.subheader("🌍 Global Revenue Distribution")

from components.executive_map import world_map

geo_col1, geo_col2 = st.columns([2, 1])

with geo_col1:
    fig_map = world_map(retail)
    st.plotly_chart(fig_map, use_container_width=True)

with geo_col2:
    country_revenue = (
        retail.groupby("Country")["Revenue"]
        .sum()
        .reset_index()
        .sort_values(by="Revenue", ascending=False)
        .head(10)
    )
    
    fig_country = px.bar(
        country_revenue,
        y="Country",
        x="Revenue",
        orientation="h",
        color="Revenue",
        color_continuous_scale="Blues",
        title="Top 10 Countries by Revenue"
    )
    fig_country.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B1120",
        plot_bgcolor="#0B1120",
        height=480,
        xaxis_title="Revenue (£)",
        yaxis_title="",
        coloraxis_showscale=False
    )
    fig_country.update_yaxes(categoryorder="total ascending")
    st.plotly_chart(fig_country, use_container_width=True)

st.divider()

# =====================================================
# PRODUCT & CUSTOMER PERFORMANCE
# =====================================================

prod_col1, prod_col2 = st.columns(2)

with prod_col1:
    st.subheader("📦 Product Performance Leaderboards")
    tab1, tab2 = st.tabs(["🔥 Top 10 Products", "❄️ Bottom 10 Products"])
    
    with tab1:
        top_products = (
            retail.groupby("ProductName")["Revenue"]
            .sum()
            .reset_index()
            .sort_values(by="Revenue", ascending=False)
            .head(10)
        )
        fig_top_prod = px.bar(
            top_products,
            x="Revenue",
            y="ProductName",
            orientation="h",
            color="Revenue",
            color_continuous_scale="GnBu",
        )
        fig_top_prod.update_layout(
            template="plotly_dark", paper_bgcolor="#0B1120", plot_bgcolor="#0B1120",
            height=400, xaxis_title="Revenue (£)", yaxis_title="", coloraxis_showscale=False
        )
        fig_top_prod.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_top_prod, use_container_width=True)
        
    with tab2:
        bottom_products = (
            retail.groupby("ProductName")["Revenue"]
            .sum()
            .reset_index()
            .sort_values(by="Revenue", ascending=True)
            .head(10)
        )
        fig_bot_prod = px.bar(
            bottom_products,
            x="Revenue",
            y="ProductName",
            orientation="h",
            color="Revenue",
            color_continuous_scale="OrRd",
        )
        fig_bot_prod.update_layout(
            template="plotly_dark", paper_bgcolor="#0B1120", plot_bgcolor="#0B1120",
            height=400, xaxis_title="Revenue (£)", yaxis_title="", coloraxis_showscale=False
        )
        fig_bot_prod.update_yaxes(categoryorder="total descending")
        st.plotly_chart(fig_bot_prod, use_container_width=True)

with prod_col2:
    st.subheader("👥 High-Value Customers")
    top_customers = (
        retail.groupby("Customer ID")["Revenue"]
        .agg(Total_Spent="sum", Order_Count="nunique")
        .reset_index()
        .sort_values(by="Total_Spent", ascending=False)
        .head(10)
    )
    # Formatted for visualization
    top_customers["Customer ID"] = top_customers["Customer ID"].astype(str)
    
    fig_cust = px.scatter(
        top_customers,
        x="Order_Count",
        y="Total_Spent",
        size="Total_Spent",
        color="Total_Spent",
        text="Customer ID",
        color_continuous_scale="Purples",
        title="Top 10 Customers (Value vs. Order Frequency)"
    )
    fig_cust.update_layout(
        template="plotly_dark", paper_bgcolor="#0B1120", plot_bgcolor="#0B1120",
        height=435, xaxis_title="Number of Orders", yaxis_title="Total Spent (£)", coloraxis_showscale=False
    )
    fig_cust.update_traces(textposition="top center")
    st.plotly_chart(fig_cust, use_container_width=True)

st.divider()

# =====================================================
# AI INSIGHTS ENGINE
# =====================================================

st.subheader("🤖 RetailPulse AI™ Executive Insights")

# Automated calculations for insights
highest_country = country_revenue.iloc[0]["Country"] if not country_revenue.empty else "N/A"
highest_product = top_products.iloc[0]["ProductName"] if not top_products.empty else "N/A"
most_valuable_customer = top_customers.iloc[0]["Customer ID"] if not top_customers.empty else "N/A"

st.markdown(f"""
<div style="background: rgba(255, 255, 255, 0.05); padding: 24px; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
    <p style="color: #3B82F6; font-weight: bold; margin-bottom: 8px;">💡 Automated Executive Summary</p>
    <ul style="color: #E2E8F0; line-height: 1.6; margin: 0; padding-left: 20px;">
        <li><b>Geographic Dominance:</b> The highest revenue-generating territory is <b>{highest_country}</b>, heavily outperforming alternate international sectors.</li>
        <li><b>Product Performance Focus:</b> <b>{highest_product}</b> is currently identified as your primary revenue engine. Replicate inventory structures to guarantee availability.</li>
        <li><b>Customer Retention Target:</b> Client ID <b>{most_valuable_customer}</b> represents the peak individual account spending. Recommend unique VIP tier retention workflows.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.divider()

# =====================================================
# DATA EXPORT HUB
# =====================================================

st.subheader("📥 Export Financial & Operations Ledger")
exp_c1, exp_c2 = st.columns(2)

with exp_c1:
    csv_data = retail.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Active View Ledger (CSV)",
        data=csv_data,
        file_name="executive_filtered_retail_ledger.csv",
        mime="text/csv",
        use_container_width=True
    )

with exp_c2:
    # Summary profile metrics download option
    summary_df = retail.groupby('Country').agg({'Revenue':'sum', 'Quantity':'sum', 'Invoice':'nunique'}).reset_index()
    csv_summary = summary_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Market Summary Profiles (CSV)",
        data=csv_summary,
        file_name="market_summary_profiles.csv",
        mime="text/csv",
        use_container_width=True
    )