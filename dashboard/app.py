import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.express as px

## Page Configuration

st.set_page_config(page_title="Crypto ETL Engine",page_icon="⚡",layout = "wide")
st.title("Live Market Intelligence Dashboard")
st.markdown("Automated multithreaded ETL pipeline tracking real-time cryptocurrency")

## The Data Pipeline
@st.cache_data(ttl=60)  # Automatically refreshes cache every 60 seconds!
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    db_path = os.path.join(project_root,"market_db.db")
    conn = sqlite3.connect(db_path)
    ## Reading the database into a DataFrame
    df = pd.read_sql("SELECT * FROM crypto_data",conn)

    conn.close()

    #Converting the timestamp string back to actual datatime objects for Plotly
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

df = load_data()

## Dashboard UI

if not df.empty:
    st.sidebar.header("PIPELINE CONTROLS")
    st.sidebar.success(f"Database Active: {len(df)} total rows")
    #number of unique coins
    unique_coins = df['coin'].unique()
    selected_coin = st.sidebar.selectbox("Target Asset",unique_coins)
    #Filtering the dataframe
    asset_df = df[df['coin'] == selected_coin].copy()

    #Get the most recent data point for the KPI cards

    st.markdown(f"### {selected_coin}")


