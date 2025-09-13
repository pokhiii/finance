import pandas as pd
from babel.numbers import format_currency

def format_inr(x: float) -> str:
    """Format a number as Indian currency (₹10,36,000.00)."""
    return format_currency(x, "INR", locale="en_IN")

def add_totals_row(df: pd.DataFrame, numeric_cols: list, label: str = "Total") -> pd.DataFrame:
    """Append a totals row at the bottom of numeric columns."""
    totals = {col: df[col].sum() if col in numeric_cols else None for col in df.columns}
    totals[df.columns[0]] = label  # Put label in first column
    df_with_total = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)
    return df_with_total
