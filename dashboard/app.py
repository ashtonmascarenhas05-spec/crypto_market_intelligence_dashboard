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

#Sidebar Navigation

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to",["Introduction","Dashboard","Tabular Display"])
st.sidebar.markdown("---")
st.sidebar.metric("Active Data Points",len(df))

# Page Logic

if page == "Introduction":
    st.title("About this Project")
    st.write("### Purpose")
    st.write("This dashboard visualizes real-time crypto market data captured via an automated ETL Pipeline")
    st.info(" DISCLAIMER:This project is strictly for educational purposes. ")

elif page == "Dashboard":
    st.title("Crypto Analytics Dashboard")


    # KPI Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Assets Tracked",len(df['coin'].unique()))
    btc_data = df[df['coin']=='bitcoin']
    if not btc_data.empty:
        latest_btc_price = btc_data['price'].iloc[-1]
        col2.metric("Latest Price (BTC)",f"${latest_btc_price:,.2f}")
    else:
        col2.metric("Latest Price (BTC)","No Data")

    # Visuals
    st.subheader("Price Trends")
    fig = px.line(df,x='timestamp',y='price',color='coin')
    st.plotly_chart(fig,use_container_width=True)

    #Comparison Chart
    st.subheader("Market Composition")
    fig_pie = px.pie(df,values='price',names='coin',title="Price Distribution")
    st.plotly_chart(fig_pie)

elif page == "Tabular Display":
    st.title("Raw Database Feed")
    st.dataframe(df, use_container_width=True)