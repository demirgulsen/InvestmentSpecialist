import pandas as pd
import  requests
import logging
from decimal import Decimal, ROUND_HALF_UP
from config.get_api_keys import exchange_rate_api_key
from config.constants import SYMBOLS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_ids_to_currency_with_exchange(amount: float, ids, vs_currencies) -> dict:
    """ Exchangerate API ile belirtilen miktarı, kaynak para biriminden hedef para birimine çevirir.

    Parameters:
        amount: float
            Çevirilecek tutar   (örn: 100.0)
        ids:  str
            Kaynak para birimi (örn: "USD")
        vs_currencies: str
            Hedef para birimi (örn: "TRY")
    Return:
        Dönüştürülmüş miktarı string olarak döndürür
        (örn: "100 USD = 3200.50 TRY")
    """

    if not exchange_rate_api_key:
        return {
            "success": False,
            "result": "API anahtarı bulunamadı!"
        }

    if amount <= 0:
        return {
            "success": False,
            "result": "Geçersiz miktar!"
        }

    # Para birimi kodlarını büyük harfe çevirir
    ids = ids.upper().strip()
    vs_currencies = vs_currencies.upper().strip()

    try:
        url = f"https://v6.exchangerate-api.com/v6/{exchange_rate_api_key}/pair/{ids.upper()}/{vs_currencies.upper()}/{amount}"
        response = requests.get(url, timeout=5)

        logger.info(f"Status Code={response.status_code}")
        if response.status_code != 200:
            return {
                "success": True,
                "result": "Kur bilgisi alınamadı."
            }

        data = response.json()
        if data.get('result') == 'success':
            logger.info(f"Response data={data}")
            rate = data["conversion_rate"]
            amount = Decimal(amount)
            rate = Decimal(rate)
            # result = amount * rate
            result = (amount * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            logger.info(f"Response result={result}")
            conversion_text = f"{amount} {ids} = {result:.2f} {vs_currencies} (Kur: {rate:.4f})"
            logger.info(f"Conversion Text: {conversion_text}")
            return {
                "success": True,
                "result": conversion_text
            }
        else:
            logger.error(f"❌ Kur Çevirme hatası: {str(response.status_code)}")
            return {
                "success": False,
                "result": f"Kur Çevirme hatası: {str(response.status_code)}"
            }

    except Exception as e:
        logger.error("❌ Kur bilgisi alınamadı.")
        return {
            "success": False,
            "result": f"Beklenmeyen bir hata oluştu {e}"
        }



def current_exchange_rates(base = "TRY"):
    """ Exchangerate API'den belirtilen kaynak para birimine göre güncel döviz kurlarını getirir.

    Parameter
        base : str
            Kaynak para birimi (örn: "TRY")

    Returns: dict
        Hedef kurların oranlarını döndürür.
        Örn: {"usd": 32.1, "eur": 0.91}
    """

    rates_url = f"https://v6.exchangerate-api.com/v6/{exchange_rate_api_key}/latest/{base}"
    response = requests.get(rates_url, timeout=5)
    response.raise_for_status()
    data = response.json()

    return data


def fetch_day7_currency_data(from_currency, to_currency):
    """ Son 7 gün için iki para birimi arasındaki çapraz kuru CoinGecko API'sinden alır.

    ⚠️ Not:
        CoinGecko doğrudan fiat (USD, EUR, TRY vb.) döviz kuru sağlamadığı için
        çapraz kur hesaplaması Bitcoin fiyatı üzerinden yapılır.
        Bu nedenle elde edilen oranlar resmi döviz kurlarından küçük farklılık gösterebilir.

    Parameters
        from_currency : str
            Kaynak para birimi (örn. "usd", "try")
        to_currency : str
            Hedef para birimi (örn. "eur", "usd")

    Returns
        pd.DataFrame | None
            Tarih ve çapraz kur oranlarını içeren DataFrame.
    """
    try:
        # Bitcoin'in 7 günlük fiyatını hem kaynak hem hedef para biriminde al
        chart_url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency={from_currency.lower()}&days=7"
        btc_from_res = requests.get(chart_url, timeout=5).json()

        chart_url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency={to_currency.lower()}&days=7"
        btc_to_res = requests.get(chart_url, timeout=5).json()

        if "prices" in btc_from_res and "prices" in btc_to_res:
            df_from = pd.DataFrame(btc_from_res["prices"], columns=["timestamp", "btc_from_price"])
            df_to = pd.DataFrame(btc_to_res["prices"], columns=["timestamp", "btc_to_price"])

            # Çapraz kur hesapla: FROM/TO = (BTC/TO) / (BTC/FROM)
            df = pd.merge(df_from, df_to, on="timestamp")
            df["rate"] = df["btc_to_price"] / df["btc_from_price"]
            df["date"] = pd.to_datetime(df["timestamp"], unit="ms").dt.date

            return df
        else:
            logger.error("API'den veri alınamadı")
            return None

    except Exception as e:
        logger.error(f"Api hatası: {e}")
        return None


# @st.cache_data(ttl=3600)
def get_available_currencies_core() -> list:
    """ Exchangerate API kullanarak desteklenen para birimlerini getirir.

    Returns:
        list[str]:
            Eğer API çağrısı başarılı olursa: Exchangerate API'nin desteklediği döviz kodlarının listesi.
                Örn: ["USD", "EUR", "GBP", "JPY", ...]
            Eğer başarısız olursa:
                Varsayılan döviz listesi döndürülür:
                ["USD", "EUR", "TRY", "GBP", "CHF", "JPY", "CAD", "KRW","QAR", "AED", "RUB", "UAH", "CNY"]

    Açıklama:
        - Fonksiyon, API'den alınan supported_codes listesini parse eder.
        - API limiti (429) veya başka bir hata durumunda güvenli bir şekilde varsayılan döviz listesi döndürülür.
        - Bu şekilde, uygulamanın döviz bilgisine ihtiyaç duyan diğer kısımları hata almadan çalışmaya devam eder.
    """
    try:
        url = f"https://v6.exchangerate-api.com/v6/{exchange_rate_api_key}/codes"
        res = requests.get(url, timeout=5)

        if res.status_code == 429:
            logger.info("Exchangerate API limiti hatası (429). Varsayılan liste döndürülüyor.")
            return SYMBOLS

        res.raise_for_status()
        data = res.json()

        if data.get("result") == "success":
            return [code for code, name in data["supported_codes"]]
        else:
            logger.info("API'den geçerli sonuç alınamadı. Varsayılan liste döndürülüyor.")
            return SYMBOLS

    except Exception as e:
        logger.info(f"Döviz API hatası: {e}. Varsayılan liste döndürülüyor.")
        return SYMBOLS

    # if data.get("result") == "success":
    #     currencies = [code for code, name in data["supported_codes"]]
    #     return f"Desteklenen para birimleri: {', '.join(currencies[:20])}... (toplam {len(currencies)} birim)"
    # else:
    #     return f"Desteklenen para birimleri: {', '.join(symbols)}"
