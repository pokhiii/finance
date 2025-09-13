import streamlit as st
import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv
from babel.numbers import format_currency

# Load environment variables from .env
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Database connection
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Fetch holdings + meta
def get_holdings_with_meta():
    conn = get_connection()
    query = """
        SELECT h.id, h.asset_name, h.asset_type, h.institution, 
               h.current_value, h.currency, h.updated_at,
               m.meta_key, m.meta_value
        FROM holdings h
        LEFT JOIN holding_meta m ON h.id = m.holding_id
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # Pivot meta into columns
    meta_pivot = df.pivot_table(
        index=["id", "asset_name", "asset_type", "institution", 
               "current_value", "currency", "updated_at"],
        columns="meta_key",
        values="meta_value",
        aggfunc="first"
    ).reset_index()

    return meta_pivot

# Streamlit UI
st.set_page_config(page_title="💼 My Holdings", layout="wide")
st.title("💼 My Holdings Dashboard")

df = get_holdings_with_meta()
st.dataframe(df, use_container_width=True)

# --- Aggregated current value by asset_type ---
agg = df.groupby("asset_type")["current_value"].sum().reset_index()

# Add percentage share
total_value = agg["current_value"].sum()
agg["percent_share"] = (agg["current_value"] / total_value) * 100

# Format Indian currency properly
def format_inr(x):
    return format_currency(x, "INR", locale="en_IN")

agg["current_value"] = agg["current_value"].apply(format_inr)
agg["percent_share"] = agg["percent_share"].map(lambda x: f"{x:.2f}%")

st.subheader("📊 Aggregated Value by Asset Type")
st.dataframe(agg, use_container_width=True)
