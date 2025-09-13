import streamlit as st
import pandas as pd
from src.data_loader import get_holdings_with_meta
from src.utils import format_inr, add_totals_row

# --- Streamlit UI ---
st.set_page_config(page_title="💼 My Holdings", layout="wide")
st.title("💼 My Holdings Dashboard")

# Fetch holdings
df = get_holdings_with_meta()

# Add totals row
df_totals = add_totals_row(df, numeric_cols=["current_value"], label="TOTAL")

# Format INR (skip NaN / non-numeric safely)
df_totals["current_value"] = df_totals["current_value"].apply(
    lambda x: format_inr(x) if pd.notnull(x) and isinstance(x, (int, float)) else x
)

st.dataframe(df_totals, use_container_width=True)

# --- Aggregated value by asset type ---
agg = df.groupby("asset_type")["current_value"].sum().reset_index()

# Add % share
total_value = agg["current_value"].sum()
agg["percent_share"] = (agg["current_value"] / total_value) * 100

agg_totals = add_totals_row(agg, numeric_cols=["current_value"], label="TOTAL")

# Format INR + %
agg_totals["current_value"] = agg_totals["current_value"].apply(
    lambda x: format_inr(x) if pd.notnull(x) and isinstance(x, (int, float)) else x
)
agg_totals["percent_share"] = agg_totals["percent_share"].map(
    lambda x: f"{x:.2f}%" if pd.notnull(x) and isinstance(x, (int, float)) else ""
)

st.subheader("📊 Aggregated Value by Asset Type")
st.dataframe(agg_totals, use_container_width=True)
