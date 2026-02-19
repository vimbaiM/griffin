"""
Enhanced URL building utilities for financial APIs
"""
import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, Optional, Type, Callable
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()


class APIProvider(Enum):
    """Supoorted API Providers"""
    ALPHA_VANTAGE = "alpha_vantage"


class URLBuilderInterface(ABC):
    """Abstract base class for URL builders"""

    @abstractmethod
    def add_params(self, params: Dict[str, str]) -> None:
        """Add parameters to the URL"""
        raise NotImplementedError

    @abstractmethod
    def build(self) -> str:
        """Build and return the complete URL"""
        raise NotImplementedError

    @property
    @abstractmethod
    def url(self) -> Optional[str]:
        """Get the built URL"""
        raise NotImplementedError


class URLBuilderFactory:
    """Factroy class for creating URL Builders"""

    registry: Dict[APIProvider, Type[URLBuilderInterface]] = {}

    @classmethod
    def create_builder(cls, provider: APIProvider) -> URLBuilderInterface:
        """Class method to create an instance of a builder class"""
        if provider not in cls.registry:
            raise ValueError(f"Unsupported API provider: {provider.value}")

        builder_class = cls.registry[provider]
        return builder_class()

    @classmethod
    def register(cls, provider: APIProvider) -> Callable:
        """Class method to register Builder class to internal registry"""

        def wrapper(builder_class: URLBuilderInterface) -> Callable:
            if provider in cls.registry:
                raise ValueError("Builder already exists")
            cls.registry[provider] = builder_class
            return builder_class

        return wrapper

    @classmethod
    def get_supported_providers(cls) -> list[APIProvider]:
        """Get list of supported API providers"""
        return list(cls.registry.keys())


@URLBuilderFactory.register(APIProvider.ALPHA_VANTAGE)
class AlphaVantageURLBuilder(URLBuilderInterface):
    """URL builder for Alpha Vantage API"""

    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        self.params = self._init_params()
        self._url: Optional[str] = None

    def _init_params(self) -> Dict[str, str]:
        """Initialize with API key"""
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY environment variable not set")
        return {"apikey": api_key}

    def add_params(self, params: Dict[str, str]) -> "AlphaVantageURLBuilder":
        """Add additional parameters with validation"""
        if not isinstance(params, dict):
            raise TypeError("Parameters must be a dictionary")

        # Validate required Alpha Vantage params
        if "function" not in params:
            raise ValueError("Alpha Vantage requires 'function' parameter")

        self.params.update(params)
        return self

    def build(self) -> str:
        """Build the complete URL"""
        query_string = urlencode(self.params)
        self._url = f"{self.BASE_URL}?{query_string}"
        return self._url

    @property
    def url(self) -> Optional[str]:
        """Get the built URL"""
        return self._url


def build_alpha_vantage_url(function: str, symbol: str = None, **kwargs) -> str:
    """Convenience function to build Alpha Vantage URLs"""
    builder = URLBuilderFactory.create_builder(APIProvider.ALPHA_VANTAGE)
    params = {"function": function}

    if symbol:
        params["symbol"] = symbol

    params.update(kwargs)
    builder.add_params(params).build()
    return builder.url
