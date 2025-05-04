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


class ExchangeAPI:
    def __init__(self, ui: FormUi):
        self.ui = ui
        self.test_API_status: int | None  = None  #test_status= for testing api failures
    
    def run(self) -> None:
        """Manages the currency conversion process flow"""
        self.ui.conversion_form()

        if not self.ui.form_has_valid_input():
            return
        
        to_currency: str = self.ui.form_values.to_currency
        amount: float = self.ui.form_values.amount
        
        exchange_data = self.fetch_exchange_rate_data(to_currency) 
        if not exchange_data:
            return
        
        result = self.calculate_result(exchange_data.rate, amount)
        self.ui.display_result(exchange_data.date, exchange_data.time, result)

    def fetch_exchange_rate_data(self, to_currency: str) -> ExchangeData | None:
        """Fetches exchange rate data. Returns: formatted data (ExchangeData) | None"""
        api_url = create_api_request("latest", to_currency)
        api_response = self.send_api_request(api_url)

        if not api_response:
            return None
        
        return self.format_data(api_response, to_currency)

    @st.cache_data
    def send_api_request(_self, api_url: str) -> dict[str, Any] | None:
        """
        Gets the API response and handles errors if status is not 200 (OK), or data is not as expected.
        Returns: API data (dict[str, Any]) | None
        """
        response: requests.Response = requests.get(api_url)
        status: int = _self.test_API_status if _self.test_API_status is not None else response.status_code
        
        if status != 200:
            _self.ui.display_error("error", f"[Status: {status}] Oops... something went wrong!")
            return None
        
        try:
            data: dict[str, Any] = response.json()
        
            if not isinstance(data, dict): # validate expected type
                _self.ui.display_error("error", "Unexpected API response format.")
                return None
            return data
        
        except ValueError:
            _self.ui.display_error("error", "Failed to parse JSON response.")
            return None

    def format_data(self, data: dict[str, Any], to_currency: str) -> ExchangeData:
        """
        Formats the json data and extracts the rate, date and time.
        Returns: rate, date, time (ExchangeData)
        """
        epoch_time: int = data["timestamp"]
        date_time: datetime = datetime.fromtimestamp(epoch_time)
        
        rate: float = data["rates"][to_currency]
        formatted_date: str = date_time.strftime("%d-%m-%Y")
        formatted_time: str = date_time.strftime("%H:%M:%S")
        
        return ExchangeData(rate=rate, date=formatted_date, time=formatted_time)

    def calculate_result(self, rate: float, amount: float) -> float |  int:
        """
        Calculates the result of the conversion from the orginal amount using the exchange rate.
        Returns: result (float | int)
        """
        result: float  = rate * amount
        return round(result, 2) if result % 1 else int(result)
