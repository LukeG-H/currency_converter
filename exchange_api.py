from form_ui import FormUi
from api_client import APIClient
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
        self.api_client = APIClient()
    
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
        """Fetches exchange rate data. Returns: formatted data [ExchangeData | None]"""
        api_url = self.api_client.create_api_request(to_currency)
        api_response = self.api_client.get(api_url)

        data, error = api_response

        if error:
            self.ui.display_error("error", error)
            return None
        
        return self.format_data(data, to_currency)

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

    def calculate_result(self, rate: float, amount: float) -> float:
        """
        Calculates the result of the conversion from the orginal amount using the exchange rate.
        Returns: result [float]
        """
        result: float  = rate * amount
        return round(result, 2)
