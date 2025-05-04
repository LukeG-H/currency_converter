import requests
import streamlit as st
from typing import *
from config import API_KEY


class APIClient:
    # ---------------------- CONSTANTS (ATTRIBUTES) ---------------------- #
    BASE_URL: str  = "http://api.exchangeratesapi.io/v1"
    ENDPOINTS: dict[str, str] = {
        "latest": "/latest", 
        "historic": "/YYYY-MM-DD"
        }
    ACCESS_KEY: str = f"?access_key={API_KEY}"
    QUERY: str = "&symbols="
    
    def __init__(self):
        self.test_API_status_response: int | None = None

    # ---------------------- STATIC METHODS ---------------------- #

    @staticmethod
    def create_api_request(symbol: str, end_point: str = "latest") -> str:
        """Creates the URL to be sent as the API request"""
        return f"{APIClient.BASE_URL}{APIClient.ENDPOINTS[end_point]}{APIClient.ACCESS_KEY}{APIClient.QUERY}{symbol}"
    
    @staticmethod
    @st.cache_data
    def _cached_request(api_url: str, test_status: int | None) -> tuple[dict[str, Any] | None, str | None]:
        """Static method used to cache API data. Returns API data[dict] | None, error[str] | None"""
        response: requests.Response = requests.get(api_url)
        status: int = test_status if test_status is not None else response.status_code

        if status != 200:
            return None, f"[Status: {status}] Oops... something went wrong!"
        
        try:
            data: dict[str, Any] = response.json()

            if not isinstance(data, dict):
                return None, "Unexpected API response format."
            return data, None
        
        except ValueError:
            return None, "Failed to parse json response"
    
    # ---------------------- INSTANCE METHODS ---------------------- # 

    def get(self, api_url: str) -> tuple[dict[str, Any] | None, str | None]:
        """Gets the API response. Returns API data[dict] | None, error[str] | None"""
        return self._cached_request(api_url, self.test_API_status_response)