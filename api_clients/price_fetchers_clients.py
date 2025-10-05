import os
import time
import requests
import logging
import yfinance as yf
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def get_currency_price(base="USD", target="TRY"):
    """ ExchangeRate API'sinden döviz kuru getirir.

    Parameters:
        base: Kaynak para birimi (örn: "USD", "EUR")
        target: Hedef para birimi (örn: "TRY", "USD")

    Returns:
        float: döviz kuru
    """
    try:
        exchange_rate_api_key = os.getenv("EXCHANGE_RATE_API")
        if not exchange_rate_api_key:
            logger.error("❌ EXCHANGE_RATE_API key bulunamadı")
            return 0.0
        # Rate limit hatasına düşmemek için her api_clients çağrısı öncesi bekleme süresi olmalı
        time.sleep(1)

        url = f"https://v6.exchangerate-api.com/v6/{exchange_rate_api_key}/latest/{base}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # response = requests.get(url, timeout=10).json()
        # return response["conversion_rates"].get(target, None)
        rate = data.get("conversion_rates", {}).get(target, 0.0)
        return float(rate) if rate else 0.0

    except requests.exceptions.RequestException as e:
        logger.error(f"❌ API isteği hatası: {e}")
        return 0.0
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {e}")
        return 0.0


def get_crypto_price(symbol: str):
    """ CoinGecko API'sinden belirtilen kripto paranın USD ve TRY cinsinden fiyatını getirir.

    Parameter:
        symbol: CoinGecko coin ID'si (örn: "bitcoin", "ethereum")

    Returns:
        float: try ve usd türünden kripto fiyatı

    Notes:
        - Rate limit: ~50 req/min.
        - Symbol→ID dönüşümü için resolve_coin_id() kullanın.
        - Örn: "BTC" → "bitcoin", "ETH" → "ethereum".
    """
    try:
        # Rate limit için bekleme
        time.sleep(1)

        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd,try"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if symbol in data:
            usd_price = data[symbol].get("usd", 0.0)  # Default 0.0
            try_price = data[symbol].get("try", 0.0)  # Default 0.0
            return  float(usd_price), float(try_price)

        logger.info(f"⚠️ {symbol} coin'i bulunamadı, 0.0 kullanılıyor")
        return 0.0, 0.0

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            logger.error("❌ Kripto Rate limit aşıldı, 40 saniye bekleniyor...")
            time.sleep(40)
            return 0.0, 0.0
        else:
            logger.error(f"❌ Kripto HTTP hatası: {e}")
            return 0.0, 0.0
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ API isteği hatası: {e}")
        return 0.0, 0.0
    except Exception as e:
        logger.error(f"❌ Beklenmeyen hata: {e}")
        return 0.0, 0.0


def get_stock_price(ticker):
    """ Yahoo Finance'den hisse senedi fiyatını getirir.

    Parameter:
        ticker: Hisse kodu (örn: "AAPL", "MSFT", "THYAO.IS")

    Returns:
        float: Kapanış fiyatı
    """
    try:
        # Rate limit için bekleme
        time.sleep(1)

        data = yf.Ticker(ticker)
        hist = data.history(period="1d")

        if not hist.empty:
            return hist["Close"].iloc[-1]

        logger.error(f"❌ {ticker} için veri bulunamadı")
        return None

    except Exception as e:
        logger.error(f"❌ Hisse fiyatı hatası ({ticker}): {e}")
        return None


def get_gold_price(vs="usd"):
    """ CoinGecko API'sinden Tether Gold (XAUT) fiyatını getirir.

    Parameter
        vs: Hedef para birimi (şu an sadece "usd" ve "try" destekleniyor).

    Açıklama:
        - XAUT, 1 ons altına eşdeğer bir kripto varlıktır.
        - Bu fonksiyon, XAUT fiyatını hem USD hem de TRY cinsinden döndürür.
        - Dönen değerler doğrudan ons fiyatıdır, gram/çeyrek gibi altın türleri için
          ayrıca dönüştürme yapılmaktadır

    Returns
        tuple[float, float]
        - (usd_fiyat, try_fiyat) şeklinde ons altın fiyatı.
    """
    try:
        # Rate limit için bekleme
        time.sleep(1)

        url = "https://api.coingecko.com/api/v3/simple/price?ids=tether-gold&vs_currencies=usd,try"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "tether-gold" not in data or vs.lower() not in data["tether-gold"]:
            logger.error("❌ Altın fiyat verisi bulunamadı")
            return 0.0, 0.0

        price_usd = data["tether-gold"].get("usd", 0.0)  # 1 XAUT fiyatı USD
        price_try = data["tether-gold"].get("try", 0.0)  # 1 XAUT fiyatı TRY

        if price_usd == 0.0 or price_try == 0.0:
            logger.error("❌ Geçersiz altın fiyatı")
            return 0.0, 0.0

        return float(price_usd), float(price_try)

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            logger.error("❌ Rate limit aşıldı, 40 saniye bekleniyor...")
            time.sleep(40)
            return 0.0, 0.0
        else:
            logger.error(f"❌ HTTP hatası: {e}")
            return 0.0, 0.0
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ API isteği hatası: {e}")
        return 0.0, 0.0
    except Exception as e:
        logger.error(f"❌ Altın fiyatı hesaplama hatası: {e}")
        return 0.0, 0.0

