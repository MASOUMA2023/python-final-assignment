import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MLB History Dashboard", layout="wide")
st.title(" MLB History Interactive Dashboard") 

@st.cache_data
def load_data():
    conn = sqlite3.connect("database/mlb_history.db")
    df = pd.read_sql_query("SELECT * FROM mlb_history", conn)
    conn.close()
    return df

df = load_data()

if df.empty:
    st.warning("No data available. Please run the scraper and DB import first.")
else:
    years = df["Year"].dropna().unique()
    selected_year = st.selectbox("Select Year", sorted(years))

    filtered = df[df["Year"] == selected_year]
    st.dataframe(filtered)

    fig = px.bar(filtered, x="Event", y="Stat", title=f"Stats for {selected_year}")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Number of Unique Events per Year")
    event_counts = df.groupby("Year")["Event"].nunique().reset_index()
    fig2 = px.line(event_counts, x="Year", y="Event", title="Unique Events Over the Years")
    st.plotly_chart(fig2, use_container_width=True)


    st.subheader("Top 10 Most Common Stats")
    top_stats = df["Stat"].value_counts().head(10).reset_index()
    top_stats.columns = ["Stat", "Count"]
    fig3 = px.bar(top_stats, x="Stat", y="Count", title="Most Frequent Stats in MLB History")
    st.plotly_chart(fig3, use_container_width=True)