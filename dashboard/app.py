import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.express as px

## Page Configuration

st.set_page_config(page_title="Crypto ETL Engine",page_icon="⚡",layout = "wide")
st.title("Market Intelligence Dashboard")
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
    
    # 1. KPI Cards (Summary)
    st.subheader("Market Overview")
    cols = st.columns(len(df['coin'].unique()))
    for i, coin in enumerate(df['coin'].unique()):
        latest_price = df[df['coin'] == coin]['price'].iloc[-1]
        cols[i].metric(f"{coin.upper()} Price", f"${latest_price:,.2f}")

    st.divider()

    # 2. Individual Line Charts (One for each coin)
    st.subheader("Price Trends per Asset")
    
    # Loop through each unique coin and create a chart
    for coin in df['coin'].unique():
        st.markdown(f"### {coin.upper()} Performance")
        
        # Filter for the specific coin
        coin_df = df[df['coin'] == coin].sort_values('timestamp')
        
        # Create the chart
        fig = px.line(
            coin_df, 
            x='timestamp', 
            y='price', 
            title=f"{coin.upper()} Live Price Trend",
            markers=True
        )
        # Add a rolling average for depth
        coin_df['Rolling_Avg'] = coin_df['price'].rolling(window=3).mean()
        fig.add_scatter(x=coin_df['timestamp'], y=coin_df['Rolling_Avg'], mode='lines', name='3-Tick Trend', line=dict(color='orange', dash='dot'))
        
        # Render the specific chart
        st.plotly_chart(fig, width='stretch')

elif page == "Tabular Display":
    st.title("Latest Feed")
    st.dataframe(df.tail(15), width='stretch')