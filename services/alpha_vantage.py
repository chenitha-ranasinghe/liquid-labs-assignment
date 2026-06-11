import os
import requests
from dotenv import load_dotenv

# load the API key from .env file
load_dotenv()

ALPHA_VANTAGE_URL = "https://www.alphavantage.co/query"

def fetch_monthly_data(symbol: str):
    # get API key from .env file
    api_key = os.getenv("ALPHAVANTAGE_API_KEY")

    # if API key missing raise Value error
    if not api_key:
        raise ValueError("ALPHAVANTAGE_API_KEY not in .env file")

    # parameters
    params = {
        "function" : "TIME_SERIES_MONTHLY", # for get monthly data
        "symbol" : symbol,  # for add symbol
        "apikey" : api_key
    }

    # Call API
    try:
        response = requests.get(ALPHA_VANTAGE_URL, params=params, timeout=10)
    except requests.exceptions.Timeout:
        raise ConnectionError("Alpha Vantage API request timed out")
    if response.status_code != 200:
        raise ConnectionError(f"Failed to reach Alpha Vantage: {response.status_code}")

    # The responses are convert to JSON dict
    data = response.json()

    #if simbol is not valid

    if "Note" in data:
        raise ConnectionError("Alpha Vantage API rate limit reached. Try again later")

    if "Information" in data:
        raise ConnectionError("Invalid API key")

    if "Monthly Time Series" not in data:
        raise ValueError(f"No data found from symbol: {symbol}")

    return data["Monthly Time Series"]




