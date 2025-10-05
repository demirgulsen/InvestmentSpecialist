import pandas as pd
from typing import List, Dict, Any


class PortfolioContext:
    """ Kullanıcının portföy bilgilerini tutar. """

    def __init__(self):
        self._data: List[Dict[str, Any]] = []
        self._timestamp: str = ""

    def set_portfolio_context(self, portfolio_data: List[Dict[str, Any]]) -> None:
        """Portföy bilgisini günceller ve zaman ekler."""
        self._data = portfolio_data
        self._timestamp = pd.Timestamp.now().isoformat()

    def get_portfolio_context(self) -> List[Dict[str, Any]]:
        """Mevcut portföy bilgisini döner."""
        return self._data

    def get_timestamp(self) -> str:
        """Son güncellenme zamanını döner."""
        return self._timestamp


# Tek bir instance oluşturup diğer yerlerde bunu kullanalım
portfolio_context = PortfolioContext()


# Alternatif yöntem
# def set_portfolio_context(portfolio_data: List[Dict[str, Any]]):
#     """Portfolio context'ini güvenli şekilde set eder"""
#     global _CURRENT_PORTFOLIO_CONTEXT
#     _CURRENT_PORTFOLIO_CONTEXT = {
#         'data': portfolio_data,
#         'timestamp': pd.Timestamp.now().isoformat()
#     }
#
# def get_portfolio_context() -> List[Dict[str, Any]]:
#     """Portfolio context'ini güvenli şekilde alır"""
#     global _CURRENT_PORTFOLIO_CONTEXT
#     return _CURRENT_PORTFOLIO_CONTEXT.get('data', [])

