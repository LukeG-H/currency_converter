from config import API_KEY
from context import *
from conversion_form import *
from typing import *
import requests
import streamlit as st


def title() -> None:
    st.title("""
    Currency Converter
    \n*Currency data updated daily*
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
def send_api_request(api_call: str, test_status: int = None) -> Union[dict, str]:
    response: requests.Response = requests.get(api_call)
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


def format_data(data: Dict[str, Any]) -> Dict[str, Any]:
    pass


def display_result(from_currency: str, to_currency: str, amount: float, result: float) -> None:
    st.subheader(f"{amount} {from_currency} = {result} {to_currency}")


def main() -> None:
    title()
    # get currencies and amount from user:
    form_input = conversion_form()
    
    if not form_input:
        return
    
    from_currency, to_currency, amount = form_input
    
    api_url = create_api_request("latest", to_currency)
    # print(api_call)
    api_response = get_api_response(api_url, test_status=404)

    if not api_response:
        return

    print(api_response)
    # result: float = get_result()
    result: float = 420.69 # placeholder value

    display_result(from_currency, to_currency, amount, result)
    
    # formatted = format_data(data)


if __name__ == "__main__":
    main()