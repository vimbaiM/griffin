"""
Data fetching APIs
"""
import os
from enum import Enum

import pandas as pd
import requests
import yfinance as yf
from cachetools.func import ttl_cache
from dotenv import load_dotenv
from fredapi import Fred

import data_loaders.utils as utils

load_dotenv()


class Topic(Enum):
    """Supported topics"""
    INFLATION = "inflation"
    INTEREST_RATES = "interest rates"
    JOBS = "jobs"
    MARKET = "market"


TOPIC_SERIES_MAP = {
    Topic.INFLATION: ["CPIAUCSL", "T10YIE"],
    Topic.INTEREST_RATES: ["FEDFUNDS", "DGS10", "MORTGAGE30US"],
    Topic.JOBS: ["UNRATE", "PAYEMS"],
    Topic.MARKET: ["SP500", "VIXCLS"],
}

SERIES_DESCRIPTION = {
    "CPIAUCSL": "Consumer Price Index for All Urban Consumers: All Items in U.S. City Average",
    "T10YIE": "10-Year Breakeven Inflation Rate",
    "FEDFUNDS": "Federal Funds Effective Rate",
    "DGS10": "Market Yield on U.S. Treasury Securities at 10-Year Constant Maturity",
    "UNRATE": "Unemployment Rate",
    "PAYEMS": "All Emplotees, Total Nonfarm",
    "SP500": "S&P 500",
    "VIXCLS": "CBOE Volatiltiy Index"
}


@ttl_cache(ttl=900)
def fetch_ticker_info(symbol: str, function: str = "OVERVIEW") -> dict:
    """Fetch ticker info from alpha vantage"""
    url = utils.build_alpha_vantage_url(function, symbol)
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


def fetch_historical_data(symbol: str, period='1y') -> pd.DataFrame:
    """Fetch historical data for a specified ticker symbol"""
    ticker = yf.Ticker(symbol)
    return ticker.history(period=period)


@ttl_cache(ttl=86_400)
def fetch_economic_data(topic: Topic) -> dict:
    """Fetch economic data based on a topic"""
    result = {}
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    fred = Fred(api_key=api_key)
    for series in TOPIC_SERIES_MAP[topic]:
        result[SERIES_DESCRIPTION[series]] = fred.get_series(
            series_id=series, observation_start='2016-01-01')
    return result
