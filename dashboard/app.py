import streamlit as st
import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(page_title="Crypto ETL", layout="wide")
st.title("⚡ Crypto ETL: Live Market Pipeline")

# 1. The Data Loader (Protected by Cache)
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    db_path = os.path.join(project_root, "market_db.db")
    
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM crypto_data", conn)
    conn.close()
    return df

# Fetch the Data
df = load_data()

# 2. Build the UI
if not df.empty:
    st.success(f"Pipeline Active: Successfully loaded {len(df)} records.")
    
    # --- SIDEBAR FILTER ---
    st.sidebar.header("Dashboard Controls")
    # Get unique coins and add a dropdown
    unique_coins = df['coin'].unique()
    selected_coin = st.sidebar.selectbox("Select Asset", unique_coins)
    
    # Filter the dataframe based on the user's selection
    filtered_df = df[df['coin'] == selected_coin]

    # --- RAW DATA TABLE ---
    st.subheader("🗄️ Raw Database Feed")
    st.dataframe(df, use_container_width=True)

    # --- STATISTICS SECTION ---
    st.subheader(f"📊 {selected_coin} Statistics")
    
    # Using Streamlit columns to put metrics side-by-side
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate Variance
        price_variance = filtered_df['price'].var()
        st.metric(label="Price Variance", value=round(price_variance, 2) if pd.notna(price_variance) else "N/A")
        
    with col2:
        # Show Correlation Matrix between raw price and log price
        st.write("Correlation: Price vs Log Price")
        corr_matrix = filtered_df[['price', 'log_price']].corr()
        st.dataframe(corr_matrix)

    # --- TIME SERIES CHART ---
    st.subheader(f"📈 {selected_coin} Price History")
    
    # Create the Matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(filtered_df['timestamp'], filtered_df['price'], label='Raw Price', color='#1f77b4', marker='o')
    
    # Add rolling average (will only show if you have > 1 row for the coin!)
    ax.plot(filtered_df['timestamp'], filtered_df['price'].rolling(window=2).mean(), label='2-Period Rolling Avg', color='#ff7f0e', linestyle='--')
    
    ax.set_title(f"{selected_coin} Price Over Time")
    ax.set_xlabel("Timestamp")
    ax.set_ylabel("Price (USD)")
    # Rotate the x-axis labels so the timestamps don't overlap
    plt.xticks(rotation=45)
    ax.legend()
    
    # Render the plot in Streamlit
    st.pyplot(fig)

else:
    st.warning("The database is currently empty. Run main.py to fetch data!")