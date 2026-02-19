"""
Tools for RAG pipeline
"""
from langchain_community.tools import tool


@tool
def fetch_stock_data():
    """From alpha vantage"""
    raise NotImplementedError

@tool
def fetch_economic_data():
    """From FRED"""
    raise NotImplementedError

@tool
def fetch_chart_data():
    """From yfinance"""
    raise NotImplementedError

@tool
def search_knowledge_base():
    """Search chroma"""
    raise NotImplementedError

@tool
def web_search():
    """Use DuckDuckGo for web search"""
    raise NotImplementedError
