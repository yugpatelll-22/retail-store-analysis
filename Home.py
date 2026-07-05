import streamlit as st

from components.theme import load_theme

from components.sidebar import sidebar

from components.filters import global_filters

from components.cards import metric_card

from utils.loader import load_data

st.set_page_config(

page_title="RetailPulse AI",

layout="wide"

)

load_theme()

sidebar()

retail,customers,forecast,inventory=load_data()

retail=global_filters(retail)

st.markdown("""

<div class="page-title">

📈 RetailPulse AI Dashboard

</div>

<div class="subtitle">

AI Powered Retail Intelligence Platform

</div>

""",unsafe_allow_html=True)

c1,c2,c3,c4=st.columns(4)

with c1:

    metric_card(

        "Revenue",

        f"£{retail['Revenue'].sum():,.0f}",

        "blue"

    )

with c2:

    metric_card(

        "Orders",

        retail['Invoice'].nunique(),

        "green"

    )

with c3:

    metric_card(

        "Customers",

        retail['Customer ID'].nunique(),

        "purple"

    )

with c4:

    metric_card(

        "Countries",

        retail['Country'].nunique(),

        "orange"

    )

st.info("✅ Module 1 completed successfully.")