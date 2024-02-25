import streamlit as st
import plotly
import plotly.express as px
import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(page_title='VOEDSEL 2023 ANALYSIS!!', page_icon=":sparkles", layout="wide")
st.title(":sparkles: VOEDSEL 2023 SALES ANALYSIS")
st.markdown('<style>div.block-container{padding-top:1.5rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder :Upload ", type=(["csv", "txt", "xlsx", "pdf"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")
else:
    os.chdir(r"C:\Users\TjTech\OneDrive\Documents\GitHub\streamlit")
    df = pd.read_csv("tobacco_sales.csv", encoding="ISO-8859-1")

col, col1 = st.columns(2)
df["Sale Date"] = pd.to_datetime(df["Sale Date"])

startDate = pd.to_datetime(df["Sale Date"]).min()
endDate = pd.to_datetime(df["Sale Date"]).max()

with col:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col1:
    date2 = pd.to_datetime(st.date_input("Start Date", endDate))

df = df[(df["Sale Date"] >= date1) & (df["Sale Date"] <= date2)]

st.sidebar.header("Choose your Province: ")
province = st.sidebar.multiselect("Pick your province", df["Province"].unique())
if not province:
    df = df.copy()
else:
    df = df[df["Province"].isin(province)]

area = st.sidebar.multiselect("Pick a Area", df["Area"].unique())
if not area:
    df2 = df.copy()
else:
    df2 = df[df["Area"].isin(area)]
if not province and not area:
    filtered_df = df
elif not area and not province:
    filtered_df = df2[df2["Area"].isin(area)]
elif not area and not province:
    filtered_df = df2[df2["Area"].isin(area)]
else:
    filtered_df = df[df["Province"].isin(province)]

category_df = filtered_df.groupby(by=["Area"], as_index=False)["US Value"].sum()

with col:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x="Area", y="US Value", text=['${:,.2f}'.format(x) for x in category_df["US Value"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True)
with col1:
    st.subheader("Region wise Sales")
    fig = px.pie(filtered_df, values="US Value", names="Area", hole=0.5)
    fig.update_traces(text=filtered_df["Area"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True,)
