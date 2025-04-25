import requests
import streamlit as st
from context import create_api_request
from form_ui import FormUi
from typing import *
from datetime import datetime
from dataclasses import dataclass

@dataclass
class ExchangeData:
    rate: float
    date: str
    time: str

def fetch_exchange_rate_data(
    to_currency: str, 
    ui: FormUi, 
    test_status: int | None = None
) -> ExchangeData | None:
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
    Gets the API response and handles errors if status is not 200 (OK), or data is not as expected.
    Returns: API data (Dict[str, Any]) | None
    """
    response: requests.Response = requests.get(api_url)
    status: int = test_status if test_status is not None else response.status_code
    
    if status != 200:
        _ui.display_error("error", f"[Status: {status}] Oops... something went wrong!")
        return
    
    try:
        data: Dict[str, Any] = response.json()
    
        if not isinstance(data, dict): # validate expected type
            _ui.display_error("error", "Unexpected API response format.")
            return
        return data
    
    except ValueError:
        _ui.display_error("error", "Failed to parse JSON response.")
        return


def format_data(data: Dict[str, Any], to_currency: str) -> ExchangeData:
    """
    Formats the json data and extracts the rate, date and time.
    Returns: rate, date, time (Tuple[float, str, str])
    """
    epoch_time: int = data["timestamp"]
    date_time: datetime = datetime.fromtimestamp(epoch_time)
    
    rate: float = data["rates"][to_currency]
    formatted_date: str = date_time.strftime("%d-%m-%Y")
    formatted_time: str = date_time.strftime("%H:%M:%S")
    
    return ExchangeData(rate=rate, date=formatted_date, time=formatted_time)


def calculate_result(rate: float, amount: float) -> float |  int:
    """
    Calculates the result of the conversion from the orginal amount using the exchange rate.
    Returns: result (float | int)
    """
    restult: float  = rate * amount
    return round(restult, 2) if restult % 1 else int(restult)
