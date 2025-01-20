from config import API_KEY
from typing import *
import requests
import streamlit as st


BASE_URL: str  = "http://api.exchangeratesapi.io/v1"
ACCESS_KEY: str = f"?access_key={API_KEY}"
ENDPOINTS: Dict[str, str] = {
    "latest": "/latest", 
    "historic": "/YYYY-MM-DD"
    }


def title() -> None:
    st.title("""
    Currency Converter
    \n**Currency data updated daily*
             """)
    
    st.subheader("Enter the currencies and amount you would like to convert:")
    
# get currencies and amount from user:
def get_currencies_form() -> Optional[Tuple[str, str, float]]:
    with st.form("conversion_form"):
        from_currency: str = st.selectbox("From Currency:", ['USD', 'AUD', 'CAD', 'PLN','MXN'])
        to_currency: str = st.selectbox("To Currency:", ['USD', 'AUD', 'CAD', 'PLN','MXN'])
        amount: float = st.number_input("Enter the amount to convert")
        submit: bool = st.form_submit_button("Convert")

    if submit:
        print(from_currency, to_currency)
        print(amount)
        return from_currency, to_currency, amount
    else:
        return None


# get the data from the api and return as json:
def get_data(end_point: str, test_status: int = None) -> Union[dict, str]:
    response: requests.Response = requests.get(BASE_URL+end_point+ACCESS_KEY)
    status: int = test_status if test_status is not None else response.status_code
    
    if status != 200:
        status_message: str = f"Oops... something went wrong! [Status: {status}]"
        return status_message
    
    # print(status)
    try:
        data: Dict[str, Any] = response.json()

        if not isinstance(data, dict): # validate expected type
            return "Unexpected API response format."
        return data
    
    except ValueError:
        return "Failed to parse JSON response."


def format_data(data: Dict[str, Any]) -> Dict[str, Any]:
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
    
    data = get_data(ENDPOINTS["latest"], test_status=404)

    if isinstance(data, str):
        st.error(data)
        st.error("Failed to fetch data. Please check your internet connection or try again later.")
        return
    # result: float = get_result()

    result: float = 420.69 # placeholder value

    display_result(from_currency, to_currency, amount, result)
    
    # formatted = format_data(data)


if __name__ == "__main__":
    main()