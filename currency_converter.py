from config import API_KEY
from context import *
from conversion_form import *
from typing import *
import requests
import streamlit as st
from datetime import datetime


def title() -> None:
    st.title("""
    Currency Converter
    \n*Currency data updated hourly*
    """)


def create_api_request(end_point: str, symbol: str) -> str:
    return f"{BASE_URL}{ENDPOINTS[end_point]}{ACCESS_KEY}{QUERY}{symbol}"


def get_api_response(api_url: str, test_status: int = None) -> Optional[dict]:
    api_response = send_api_request(api_url, test_status)

    if isinstance(api_response, str):
        st.error(api_response)
        st.error("Failed to fetch data. Please check your internet connection or try again later.")
        return None
    
    return api_response


# get the data from the api and return as json, unless status is not 200:
@st.cache_data
def send_api_request(api_url: str, test_status: int = None) -> Union[dict, str]:
    response: requests.Response = requests.get(api_url)
    status: int = test_status if test_status is not None else response.status_code
    
    if status != 200:
        status_message: str = f"Oops... something went wrong! [Status: {status}]"
        return status_message
    
    try:
        data: Dict[str, Any] = response.json()

        if not isinstance(data, dict): # validate expected type
            return "Unexpected API response format."
        return data
    
    except ValueError:
        return "Failed to parse JSON response."


def format_data(data: Dict[str, Any], to_currency: str) -> Dict[str, Any]:
    epoch_time = data["timestamp"]
    formatted_time: object = datetime.fromtimestamp(epoch_time)
    rate: float = data["rates"][to_currency]
    # print(rate)
    # print(formatted_time)
    return rate, formatted_time


def calculate_result(rate: float, amount: float) -> float:
    return round(rate * amount, 2)

def display_result(from_currency: str, to_currency: str, date_time: object, amount: float, result: float) -> None:
    # col1, col2 = st.columns(2,gap='small')
    # col1.write(f"As of {date_time}")
    # col2.write(f"{amount} {from_currency} = {result} {to_currency}")
    
    st.subheader(f"{amount} {from_currency} = {result} {to_currency}", divider="green",)
    st.text(f"As of {date_time}")


def main() -> None:
    title()
    # get currencies and amount from user:
    form_input = conversion_form()
    
    if not form_input:
        return
    
    from_currency, to_currency, amount = form_input

    api_url = create_api_request("latest", to_currency)

    # use test_status= for testing
    api_response = get_api_response(api_url)
    # api_response = send_api_request(api_url)
    
    # if isinstance(api_response, str):
    #     st.error(api_response)
    #     st.error("Failed to fetch data. Please check your internet connection or try again later.")
    #     return
    
    if not api_response:
        return

    rate, date_time  = format_data(api_response, to_currency)
    result = calculate_result(rate, amount)
    # result: float = 420.69 # placeholder value

    display_result(from_currency, to_currency, date_time, amount, result)


if __name__ == "__main__":
    main()