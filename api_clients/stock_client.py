import pandas as pd
import  requests
import logging
import yfinance as yf
from datetime import datetime, timedelta
from config.get_api_keys import exchange_rate_api_key, finn_api_key

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_stock_data_core(ticker: str) -> dict:
    """ Finnhub API'den güncel hisse senedi bilgilerini dict olarak getirir.

    Parameter:
        ticker (str) : Hisse senedi sembolü (örn: "AAPL", "GOOGL", "TSLA")
    Return:
        dict: Güncel hisse bilgileri
    """
    try:
        if not finn_api_key:
            logger.error("❌ API anahtarı bulunamadı. FINNHUB_API_KEY environment variable'ını kontrol edin.")
            return {"error": "API anahtarı bulunamadı."}

        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={finn_api_key}"
        resource = requests.get(url, timeout=5)
        logger.info(f"Status Code: {resource.status_code}")  # Debug için

        if resource.status_code == 429:
            return {"error": "API limiti aşıldı!"}

        if resource.status_code != 200:
            logger.info(f"❌ API Hatası: {resource.status_code}")
            return {"error": f"API Hatası: {resource.status_code}"}

        data = resource.json()
        if not data or data.get('c') is None:
            logger.info(f"❌ {ticker} hissesi için veri bulunamadı. Lütfen hisse sembolünü kontrol edin!")
            return {"error": "Veri alınamadı. Lütfen hisse sembolünü kontrol edin!"}

        return {
            "ticker": ticker.upper(),
            "success": True,
            "current_price": data["c"],
            "change": data["d"],
            "change_percent": data["dp"],
            "open": data["o"],
            "high": data["h"],
            "low": data["l"],
        }


    except Exception as e:
        logger.error(f"{ticker} verisi alınırken hata oluştu: {e}")
        return {
            "ticker": ticker.upper(),
            "success": False,
            "error": str(e)
        }


def get_7day_stock_history(stock_symbol: str) -> pd.DataFrame:
    """ Belirtilen hisse senedinin son 7 günlük kapanış fiyatlarını getirir.

    Parameter:
        stock_symbol (str): Hisse senedi sembolü (örn. 'AAPL')
    Return:
        pd.DataFrame: Tarih indeksli kapanış fiyatları
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=7)

    ticker = yf.Ticker(stock_symbol)
    df = ticker.history(start=start_date, end=end_date)

    return df