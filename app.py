import streamlit as st
import pandas as pd
from src.data_loader import get_holdings_with_meta
from src.utils import format_inr

# --- Streamlit UI ---
st.set_page_config(page_title="💼 My Holdings", layout="wide")
st.title("💼 My Holdings Dashboard")

# Fetch holdings
df = get_holdings_with_meta()
st.dataframe(df, use_container_width=True)

# --- Aggregated value by asset type ---
agg = df.groupby("asset_type")["current_value"].sum().reset_index()

# Add % share
total_value = agg["current_value"].sum()
agg["percent_share"] = (agg["current_value"] / total_value) * 100

# Format
agg["current_value"] = agg["current_value"].apply(format_inr)
agg["percent_share"] = agg["percent_share"].map(lambda x: f"{x:.2f}%")

st.subheader("📊 Aggregated Value by Asset Type")
st.dataframe(agg, use_container_width=True)
