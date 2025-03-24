import requests
import streamlit as st
from context import create_api_request
from form_ui import title, conversion_form, display_result
from typing import *
from datetime import datetime


# Fetch and return formatted exchange rate data, or return none if error
def fetch_exchange_rate_data(to_currency: str, test_status: Optional[int] = None) -> Optional[Tuple[float, str, str]]:
    api_url = create_api_request("latest", to_currency)
    api_response = send_api_request(api_url, test_status)

    if not api_response:
        st.error("Failed to retreive exchange rate data.")
        return
    
    return format_data(api_response, to_currency)


# Send the API request and return data as json dict, otherwise handle error and return none
@st.cache_data
def send_api_request(api_url: str, test_status: Optional[int] = None) -> Optional[Dict[str, Any]]:
    response: requests.Response = requests.get(api_url)
    status: int = test_status if test_status is not None else response.status_code
    
    if status != 200:
        st.error(f"[Status: {status}] Oops... something went wrong!")
        return
    
    try:
        data: Dict[str, Any] = response.json()

        if not isinstance(data, dict): # validate expected type
            st.error("Unexpected API response format.")
            return
        return data
    
    except ValueError:
        print("Failed to parse JSON response.")
        return


# Format json data to return just the rate and the datetime
def format_data(data: Dict[str, Any], to_currency: str) -> Tuple[float, str, str]:
    epoch_time: int = data["timestamp"]
    rate: float = data["rates"][to_currency]
    
    date_time: datetime = datetime.fromtimestamp(epoch_time)
    formatted_date: str = date_time.strftime("%d-%m-%Y")
    formatted_time: str = date_time.strftime("%H:%M:%S")
    
    return rate, formatted_date, formatted_time


# Calculate the conversion using rate from API
def calculate_result(rate: float, amount: float) -> Union[float, int]:
    restult = rate * amount
    return round(restult, 2) if restult % 1 else int(restult)


def main() -> None:
    title()
    form_input = conversion_form()
    if not form_input:
        return
    
    from_currency, to_currency, amount = form_input

    exchange_data = fetch_exchange_rate_data(to_currency) #test_status= for testing api failures
    if not exchange_data:
        return
    
    rate, date, time = exchange_data
    
    result = calculate_result(rate, amount)
    display_result(from_currency, to_currency, amount, date, time, result)


if __name__ == "__main__":
    main()