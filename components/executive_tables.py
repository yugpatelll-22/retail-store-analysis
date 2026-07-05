import pandas as pd


def top_products(df):

    return (

        df.groupby("ProductName")["Revenue"]

        .sum()

        .sort_values(ascending=False)

        .head(10)

        .reset_index()

    )


def top_customers(df):

    return (

        df.groupby("Customer ID")

        .agg(

            Revenue=("Revenue", "sum"),

            Orders=("Invoice", "nunique"),

            Country=("Country", "first")

        )

        .sort_values("Revenue", ascending=False)

        .head(10)

        .reset_index()

    )