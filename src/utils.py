from babel.numbers import format_currency

def format_inr(x: float) -> str:
    """Format a number as Indian currency (₹10,36,000.00)."""
    return format_currency(x, "INR", locale="en_IN")
