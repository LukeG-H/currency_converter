from exchange_api import fetch_exchange_rate_data, calculate_result, ExchangeData
from form_ui import FormUi
from typing import *


def main() -> None:
    ui: FormUi = FormUi()
    ui.conversion_form()

    if not ui.form_has_valid_input():
        return
    
    to_currency: str = ui.form_values["to_currency"]
    amount: float = ui.form_values["amount"]

    exchange_data: ExchangeData | None = fetch_exchange_rate_data(to_currency, ui) #test_status= for testing api failures
    if not exchange_data:
        return
    
    result = calculate_result(exchange_data.rate, amount)
    ui.display_result(exchange_data.date, exchange_data.time, result)


if __name__ == "__main__":
    main()