import plotly.express as px
import pandas as pd


# Revenue Trend
def revenue_trend(df):

    monthly = (
        df.groupby(
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

        color_discrete_sequence=["#3B82F6"]

    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0B1120",

        plot_bgcolor="#0B1120",

        height=420,

        xaxis_title="",

        yaxis_title="Revenue (£)",

        font=dict(color="white")

    )

    return fig



# Monthly Sales
def monthly_sales(df):

    monthly = (
        df.groupby(df["InvoiceDate"].dt.month_name())["Revenue"]
        .sum()
        .reset_index()
    )

    order = [
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

    monthly["InvoiceDate"] = pd.Categorical(
        monthly["InvoiceDate"],
        order,
        ordered=True
    )

    monthly = monthly.sort_values("InvoiceDate")

    fig = px.bar(

        monthly,

        x="InvoiceDate",

        y="Revenue",

        color="Revenue",

        color_continuous_scale="Blues"

    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0B1120",

        plot_bgcolor="#0B1120",

        height=420,

        xaxis_title="",

        yaxis_title="Revenue (£)",

        font=dict(color="white")

    )

    return fig