import streamlit as st
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_all_coins():
    """ CoinGecko'dan tüm coin listesini getirir.

    Returns:
        list: Tüm coin listesi [{"id": "bitcoin", "name": "Bitcoin", ...}]
    """
    try:
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        logging.error(f"❌ Coin listesi alınamadı: {e}")
        return []

@st.cache_data(ttl=3600)
def get_all_coins_cached():
    """ CoinGecko API'sinden kripto para listesini alır ve 1 saat boyunca önbelleğe kaydeder.

    Returns:
        list: Kripto para adlarını ve sembollerini içeren liste.
    """
    time.sleep(0.5)
    return get_all_coins()


def resolve_coin_id(asset: str, coins: list[dict]) -> str | None:
    """ Kullanıcının girdiği varlık adını (ör. Bitcoin, Ethereum) CoinGecko API’sindeki resmi coin kimliği (ID) ile eşleştirir.
        Bu ID, API çağrılarında kullanılır.

    Parameters:
        asset: Coin adı veya ID'si (örn: "Bitcoin", "bitcoin", "BTC")
        coins: CoinGecko coins listesi

    Note:
        Önce name yoksa symbol yoksa id eşleşmesine bakar.
    """
    # symbols = get_coin_id_from_symbol(asset, coins)
    # matches = [coin_id for coin_id, sym in symbols.items() if sym.lower() == asset.strip().lower()]

    for c in coins:
        # 1) name tam eşleşme
        if c.get("name").strip() == asset.strip():
            print("coin name", c.get("name"))
            return c["id"]

        # 2) id tam eşleşme
        elif c.get("id") == asset.strip().lower():
            print("coin id ", c["id"])
            return c["id"]

        # # 3) symbol tam eşleşme
        # elif matches:
        #     print("Eşleşen id:", matches[0])  # bitcoin
        #     return matches[0]

    print("Lütfen önerilen isim formatına dikkat edin!")
    return None


# NOT:
# get_coin_id_from_symbol fonksiyonu, BTC gibi sembol girişlerinde bitcoin gibi id bilgilerini almak için yazıldı.
# Lakin birden fazla 'btc' symbol'üne ait değer döndüğü için ilgili id çekilemedi.

# def get_coin_id_from_symbol(symbol: str, coins: list[dict]) -> dict | None:
#     """
#     Coin sembolünden CoinGecko ID'si bulur.
#
#     Parameter
#     ----------
#         symbol: Coin sembolü (örn: "BTC", "ETH")
#
#     Returns
#     -------
#         str: Coin ID'si (örn: "bitcoin")
#         None: Bulunamazsa
#     """
#     try:
#         symbol_dict={}
#         for col in coins:
#             if col.get("symbol", "").lower() == symbol.lower():
#                 symbol_dict[col["id"]] = col["symbol"]
#
#         if not symbol_dict:
#             print("Kripto ismini kontrol edin ve tekrar deneyin!")
#             return None
#
#         return symbol_dict
#
#     except Exception as e:
#         print(f"❌ Beklenmeyen hata: {e}")
#         return None
#