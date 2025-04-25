import requests
import streamlit as st
from context import create_api_request
from form_ui import FormUi
from typing import *
from datetime import datetime


def fetch_exchange_rate_data(
    to_currency: str, 
    ui: FormUi, 
    test_status: int | None = None
) -> Tuple[float, str, str] | None:
    """
    Uses create_api_request & send_api_request to fetch exchange rate data.
    Returns: formatted data (Tuple[float, str, str]) | None
    """
    api_url = create_api_request("latest", to_currency)
    api_response = send_api_request(api_url, ui, test_status)

    if not api_response:
        return
    
    return format_data(api_response, to_currency)


@st.cache_data
def send_api_request(
    api_url: str, 
    _ui: FormUi, 
    test_status: int | None = None
) -> Dict[str, Any] | None:
    """
    Gets the api response and handles errors if status is not 200 (OK), or data is not as expected.
    Returns: api data (Dict[str, Any]) | None
    """
    response: requests.Response = requests.get(api_url)
    status: int = test_status if test_status is not None else response.status_code
    
    if status != 200:
        _ui.display_error(f"[Status: {status}] Oops... something went wrong!")
        return
    
    try:
        data: Dict[str, Any] = response.json()

        if not isinstance(data, dict): # validate expected type
            _ui.display_error("Unexpected API response format.")
            return
        return data
    
    except ValueError:
        _ui.display_error("Failed to parse JSON response.")
        return


def format_data(data: Dict[str, Any], to_currency: str) -> Tuple[float, str, str]:
    """
    Formats the json data and extracts the rate, date and time.
    Returns: rate, date, time (Tuple[float, str, str])
    """
    epoch_time: int = data["timestamp"]
    rate: float = data["rates"][to_currency]
    
    date_time: datetime = datetime.fromtimestamp(epoch_time)
    formatted_date: str = date_time.strftime("%d-%m-%Y")
    formatted_time: str = date_time.strftime("%H:%M:%S")
    
    return rate, formatted_date, formatted_time


def calculate_result(rate: float, amount: float) -> float |  int:
    """
    Calculates the result of the conversion from the orginal amount using the exchange rate.
    Returns: result (float | int)
    """
    restult: float  = rate * amount
    return round(restult, 2) if restult % 1 else int(restult)


def main() -> None:
    ui: FormUi = FormUi()
    ui.conversion_form()

    if not ui.form_has_valid_input():
        return
    
    from_currency: str = ui.form_values["from_currency"]
    to_currency: str = ui.form_values["to_currency"]
    amount: float = ui.form_values["amount"]

    exchange_data = fetch_exchange_rate_data(to_currency, ui) #test_status= for testing api failures
    if not exchange_data:
        return
    
    rate, date, time = exchange_data
    result = calculate_result(rate, amount)

    ui.display_result(
        from_currency, 
        to_currency,
        amount, 
        date, 
        time, 
        result
        )


if __name__ == "__main__":
    main()