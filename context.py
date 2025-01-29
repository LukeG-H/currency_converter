from typing import *
from config import API_KEY

BASE_URL: str  = "http://api.exchangeratesapi.io/v1"
ENDPOINTS: Dict[str, str] = {
    "latest": "/latest", 
    "historic": "/YYYY-MM-DD"
    }
ACCESS_KEY: str = f"?access_key={API_KEY}"
QUERY: str = "&symbols="