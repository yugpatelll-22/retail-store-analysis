import streamlit as st


def metric_card(title,value,color):

    st.markdown(f"""

<div class="metric-card">

<div class="metric-title">

{title}

</div>

<div class="metric-value {color}">

{value}

</div>

</div>

""",unsafe_allow_html=True)