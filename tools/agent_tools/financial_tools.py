import logging
from langchain_core.tools import tool
from api_clients.currency_clients import convert_ids_to_currency_with_exchange
from services.stock_services import format_stock_data_for_agent
# from ai_agent.portfolio.portfolio_context_manager import PortfolioContext

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def convert_currency_for_exchange(amount: float, from_currency: str, to_currency: str) -> str:
    """ Belirtilen miktarı kaynak para biriminden hedef para birimine çevirir.

    Parameters:
        amount (float): Çevirilecek miktar (kullanıcının belirttiği tam miktar)
        from_currency (str): Kaynak para birimi kodu (USD, EUR, TRY vb.)
        to_currency (str): Hedef para birimi kodu (USD, EUR, TRY vb.)

    Return: Currency conversion data (schema: CURRENCY_FORMAT)
    +
    💵 **GÜNCEL DÖVİZ KURU**
    🇺🇸 [amount] [from_currency] = [result] [to_currency] 🇹🇷
    +
    📈 **KUR ANALİZİ:** :
    - Kur seviyesi değerlendirmesi
    - Trend analizi
    - Ekonomik faktörler
    - Yatırımcı için öneriler
    """
    try:
        amount = float(amount)
        if amount <= 0:
            return "Geçersiz miktar - pozitif bir sayı giriniz."

        # Para birimi kodlarını standardize et
        from_currency = str(from_currency).upper().strip()
        to_currency = str(to_currency).upper().strip()
        raw_result = convert_ids_to_currency_with_exchange(amount, from_currency, to_currency)

        if raw_result.get("success"):
            return f"GÜNCEL DÖVİZ KURU:\n 🇺🇸 {amount:,.2f} {from_currency} = {raw_result['result']} {to_currency} 🇹🇷"
        else:
            return f"GÜNCEL DÖVİZ KURU:\n {raw_result['result']}"

    except (ValueError, TypeError) as e:
        return f"Geçersiz giriş parametresi: {str(e)}"
    except Exception as e:
        return f"Çevrim hatası: {e}"


@tool
def get_stock_data(symbol: str) -> str:
    """ Belirlenen hisse senedinin güncel fiyatını ve piyasa bilgilerini getirir.

    Parametre:
        symbol: Hisse senedi sembolü (string, örn: AAPL, AMZN, TSLA, GOOGL vb.)

    Returns: Raw conversion data (use STOCK_FORMAT)
    +
    📈 **HISSE ANALİZİ**
    - Güncel fiyat bilgileri
    - Değişim oranları
    - Piyasa performansı
    - Kısa vadeli değerlendirme
    """

    try:
        logger.info(f"get_stock_data çağrıldı, symbol: {symbol}")

        if not symbol or not isinstance(symbol, str):
            return "Geçersiz hisse sembolü"

        result = format_stock_data_for_agent(symbol)

        # Eğer başarısızsa web araması yap
        if any(keyword in result.lower() for keyword in ['hata', 'bulunamadı', 'api_clients hatası']):
            return f"Hisse verisi alınamadı: {result}\n Web araması önerilir."

        return result

    except Exception as e:
        print(f"DEBUG: Hata oluştu: {str(e)}")
        return f"Hisse verisi alınamadı. Web araması önerilir: {e}"
