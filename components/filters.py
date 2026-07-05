import streamlit as st


def global_filters(df):

    st.sidebar.header("Filters")

    countries = st.sidebar.multiselect(

        "Country",

        sorted(df["Country"].dropna().unique()),

        default=sorted(df["Country"].dropna().unique())

    )

    years = st.sidebar.multiselect(

        "Year",

        sorted(df["InvoiceDate"].dt.year.unique()),

        default=sorted(df["InvoiceDate"].dt.year.unique())

    )

    filtered = df[

        (df["Country"].isin(countries))

        &

        (df["InvoiceDate"].dt.year.isin(years))

    ]

    return filtered