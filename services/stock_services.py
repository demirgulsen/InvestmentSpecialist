import logging
from api_clients.stock_client import get_stock_data_core

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_stock_data_for_agent(ticker: str) -> str:
    """ get_stock_data_core çıktısını metin formatına çevirir (agent için).

    Parameter:
        ticker (str) : Hisse senedi sembolü (örn: "AAPL", "GOOGL", "TSLA")
    """
    data = get_stock_data_core(ticker)

    if "error" in data:
        return f"{ticker} için hata: {data['error']}"

     return f"""
        {ticker.upper()} Hisse Senedi: \n
        • Güncel Fiyat: ${data['current_price']:.2f} \n
        • Değişim: ${data['change']:.2f} ({data['change_percent']:.2f}%) \n
        • Açılış Fiyatı: ${data['open']:.2f} \n
        • Gün İçi En Yüksek: ${data['high']:.2f} \n
        • Gün İçi En Düşük: ${data['low']:.2f} \n
    """.strip()
