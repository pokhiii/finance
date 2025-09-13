import pandas as pd
from .db import get_connection

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
