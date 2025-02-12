import streamlit as st
from currencies import CURRENCY_OPTIONS
from typing import *


#  UI Title
def title() -> None:
    st.title("""
    Currency Converter\n*Currency data updated hourly*
    """)


# Conversion form for user inputs
def conversion_form() -> Optional[Tuple[str, str, float]]:
    with st.form("conversion_form"):
        from_currency: str = st.selectbox("From Currency:", ['EUR'])
        to_currency: str = st.selectbox("To Currency:", CURRENCY_OPTIONS, index=CURRENCY_OPTIONS.index("USD"))
        amount: float = st.number_input("Enter the amount to convert")
        submit: bool = st.form_submit_button("Convert")
    
    if submit:
        if amount <= 0.00:
            st.warning("Enter an amount higher than 0.00 and click [Convert]")
            return None
        return from_currency, to_currency, amount
    
    st.warning("Fill out the fields above and click [Convert]")
    return None


# Display the results of the conversion
def display_result(from_currency: str, to_currency: str, amount: float, date: str, time: str,  result: float) -> None:
    # col1, col2 = st.columns(2,gap='small')
    # col1.write(f"As of {date_time}")
    # col2.write(f"{amount} {from_currency} = {result} {to_currency}")
    
    st.subheader(f"{amount} {from_currency} = {result} {to_currency}", divider="green")
    st.text(f"""As of: {date} {time}""")