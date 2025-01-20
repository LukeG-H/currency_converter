from config import API_KEY
from typing import *
import requests
import streamlit as st


BASE_URL: str  = "http://api.exchangeratesapi.io/v1"
ACCESS_KEY: str = f"?access_key={API_KEY}"
LATEST: str = "/latest"
HISTROICAL: str = "/YYYY-MM-DD"


def title() -> None:
    st.write("""
    # Currency Converter
    \n**Currency data updated daily*
             """)
    

def get_currencies_form() -> Optional[Tuple[str, str, float]]:
    st.subheader("Enter the currencies and amount you would like to convert:")
    with st.form("conversion_form"):
        from_currency: str = st.selectbox("From Currency:", ['USD', 'AUD', 'CAD', 'PLN','MXN'])
        to_currency: str = st.selectbox("To Currency:", ['USD', 'AUD', 'CAD', 'PLN','MXN'])
        amount: float = st.number_input("Enter the amount to convert")
        submit: bool = st.form_submit_button("Convert")

    if submit:
        print(from_currency, to_currency)
        print(amount)
        return from_currency, to_currency, amount
    return None


def get_data(end_point: str, test_status: int = None) -> dict:
    response: requests.Response = requests.get(BASE_URL+end_point+ACCESS_KEY)
    status = response.status_code
    data = response.json()
    print(status)


def format_data(data: dict) -> dict:
    pass


def display_result(from_currency: str, to_currency: str, amount: float, result: float) -> None:
    st.subheader(f"{amount} {from_currency} = {result} {to_currency}")

def main() -> None:
    title()
    form_input = get_currencies_form()
    
    if form_input is None:
        st.warning("Fill out the fields above and click [Convert]")
        return
    
    from_currency, to_currency, amount = form_input
    
    # data = get_data(LATEST)
    # result: float = get_result()
    
    result = 420.69 # placeholder value

    display_result(from_currency, to_currency, amount, result)
    
    # formatted = format_data(data)


if __name__ == "__main__":
    main()