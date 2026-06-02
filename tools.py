"""
Tools for RAG pipeline
"""
from langchain_community.tools import DuckDuckGoSearchRun, tool

from vectorstore import retriever


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
def retrieve_educational_content(query: str) -> str:
    """Search chroma"""
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])


def web_search(query):
    """Use DuckDuckGo for web search. Verify implementation"""
    search = DuckDuckGoSearchRun()
    return search.run(query)