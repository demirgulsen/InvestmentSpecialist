import streamlit as st
from api_clients.currency_clients import convert_ids_to_currency_with_exchange, current_exchange_rates
from api_clients.currency_clients import get_available_currencies_core
from config.constants import CURRENCY_SYMBOLS


def get_exchange_currency(amount, from_currency, to_currency):
    """ Belirtilen miktarı, kaynak para biriminden hedef para birimine dönüştürür. """
    return convert_ids_to_currency_with_exchange(amount, from_currency, to_currency)


# conversion_text = convert_ids_to_currency_for_coingecko(amount, from_currency, to_currency)
def get_current_exchange_rates():
    """ Exchangerate API üzerinden güncel döviz kurlarını alır ve her 1 birim
        döviz için kaç TRY ettiğini hesaplayarak bir sözlük olarak döndürür.
    """
    data = current_exchange_rates()
    if data.get("result") == "success":
        # 1 birim döviz kaç TRY
        return {cur: 1 / data["conversion_rates"][cur] for cur in CURRENCY_SYMBOLS.keys()}

    return None


# portfolio
@st.cache_data(ttl=3600)  # 1 saat cache, ttl=None yaparak sonsuz tutulabilir
def get_currencies_from_api():
    """ Exchangerate API’den desteklenen döviz kodlarını getirir.

    Bu fonksiyon, `get_available_currencies_core()` fonksiyonunun bir alias'ıdır.
        - API çağrısını yapar ve başarılı olursa döviz kodlarını listeler.
        - Başarısız olursa varsayılan döviz listesi döner.
    """
    return get_available_currencies_core()


