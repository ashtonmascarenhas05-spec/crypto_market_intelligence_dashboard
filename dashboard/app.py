import streamlit as st
import sqlite3 
import pandas as pd
import os

#Configuration of Page
st.set_page_config(page_title="Crypto ETL",layout="wide")
st.title("Crypto ETL: Live Market Pipeline")

# The Data Loader (Protected by a Decorator)
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    db_path = os.path.join(project_root,"market_db.db")
    conn = sqlite3.connect(db_path)
    # Converting the data from the Database into a DataFrame
    df = pd.read_sql("SELECT * FROM crypto_data",conn)
    conn.close()
    return df

df = load_data()

if not df.empty:
    st.success(f"Pipeline Active: Successfully loaded {len(df)} records from the database.")
    st.subheader("Raw Database Feed")
else:
    st.warning("The database is currently empty. Run main.py to fetch the data!")