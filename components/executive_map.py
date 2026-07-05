import plotly.express as px


def world_map(df):

    country = (
        df.groupby("Country")
        .agg(
            Revenue=("Revenue", "sum"),
            Orders=("Invoice", "nunique"),
            Customers=("Customer ID", "nunique")
        )
        .reset_index()
    )

    fig = px.choropleth(

        country,

        locations="Country",

        locationmode="country names",

        color="Revenue",

        hover_name="Country",

        hover_data=[
            "Revenue",
            "Orders",
            "Customers"
        ],

        color_continuous_scale="Blues"

    )

    fig.update_layout(

        template="plotly_dark",

        paper_bgcolor="#0B1120",

        geo_bgcolor="#0B1120",

        height=520,

        font=dict(color="white")

    )

    return fig