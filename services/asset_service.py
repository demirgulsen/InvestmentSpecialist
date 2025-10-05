import logging
from api_clients.price_fetchers_clients import get_currency_price, get_crypto_price, get_stock_price, get_gold_price
from api_clients.coingecko_clients import get_all_coins_cached, resolve_coin_id
from config.constants import MAPPING_GOLD
from config.constants import GRAM_PER_OUNCE, GOLD_22K_PURITY, QUARTER_GOLD_WEIGHT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_currency_asset_price(asset: str) -> tuple[float, float]:
    """ Döviz fiyatını USD ve TRY cinsinden döndürür. """
    try:
        usd_price = get_currency_price(asset.upper(), "USD")
        try_price = get_currency_price(asset.upper(), "TRY")
        if usd_price > 0 and try_price > 0:
            logging.info(f"Döviz fiyatı ({asset}): {usd_price} (USD), {try_price} (TRY)")
            return usd_price, try_price
        else:
            logging.error(f"❌ Geçersiz döviz kuru: {asset}")
            return 0.0, 0.0

    except Exception as e:
        logging.error(f"Döviz fiyatı alınamadı ({asset}): {e}")
        return 0.0, 0.0


def get_crypto_asset_price(asset: str) -> tuple[float, float]:
    """ Kripto fiyatını USD ve TRY cinsinden döndürür. """
    try:
        coins = get_all_coins_cached()
        coin_id = resolve_coin_id(asset, coins)
        if coin_id:
            usd_price, try_price = get_crypto_price(coin_id)
            if usd_price > 0 and try_price > 0:
                logging.info(f"Kripto fiyatı ({asset}): {usd_price} (USD), {try_price} (TRY)")
                return usd_price, try_price
            else:
                logging.error(f"❌ Geçersiz kripto fiyatı: {asset}")
                return 0.0, 0.0
        else:
            logging.error(f"❌ Kripto coin ID bulunamadı: {asset}")
            return 0.0, 0.0

    except Exception as e:
        logging.error(f"❌ Kripto fiyatı alınamadı ({asset}): {e}")
        return 0.0, 0.0


def get_stock_asset_price(asset: str) -> tuple[float, float]:
    """ Hisse fiyatını USD ve TRY cinsinden döndürür. """
    try:
        usd_price = get_stock_price(asset)
        print("Hisse fiyatı (dolar türünen)", usd_price)
        if usd_price and usd_price > 0:
            # usd -> try dönüşümü yapalım
            convert_price = get_currency_price("USD", "TRY")
            if convert_price > 0:
                try_price = usd_price * convert_price
                print(f"Hisse fiyatı ({asset}): {usd_price} (USD), {try_price} (TRY)")
                return usd_price, try_price
            else:
                logging.error("❌ USD/TRY kuru alınamadı")
                return 0.0, 0.0
        else:
            logging.error(f"❌ Hisse fiyatı alınamadı: {asset}")
            return 0.0, 0.0
    except Exception as e:
        logging.error(f"❌ Hisse fiyatı hatası ({asset}): {e}")
        return 0.0, 0.0


def get_gold_asset_price(asset: str, base_currency="TRY") -> tuple[float, float]:
    """ Altın fiyatını USD ve TRY cinsinden döndürür. """
    try:
        usd_price, try_price = calculate_gold_price(MAPPING_GOLD[asset], base_currency)
        if usd_price > 0 and try_price > 0:
            logging.info(f"Altın fiyatı ({asset}): {usd_price} (USD), {try_price} (TRY)")
            return usd_price, try_price
        else:
            logging.error(f"❌ Geçersiz altın fiyatı: {asset}")
            return 0.0, 0.0
    except Exception as e:
        logging.error(f"❌ Altın fiyatı alınamadı ({asset}): {e}")
        return 0.0, 0.0


def calculate_gold_price(gold_type: str, vs) -> tuple[float, float]:
    """ XAUT fiyatından farklı altın türlerini hesaplar.
    Parameter
        gold_type: Altın türü ("gram", "gram22", "çeyrek", "ons")
        vs: Hedef para birimi (örn: "usd", "try")
    """

    price_usd, price_try = get_gold_price(vs)
    gram_24k_usd = price_usd / GRAM_PER_OUNCE  # 1 XAUT ≈ 1 ons (GRAM_PER_OUNCE = 31.1034768 gram)
    gram_24k_try = price_try / GRAM_PER_OUNCE

    if gold_type.lower() == "gram-22":
        return (gram_24k_usd * GOLD_22K_PURITY,
                gram_24k_try * GOLD_22K_PURITY)  # GOLD_22K_PURITY = 0.916
    elif gold_type.lower() == "gram-24":
        return gram_24k_usd, gram_24k_try
    elif gold_type.lower() == "ceyrek":
        return (gram_24k_usd * QUARTER_GOLD_WEIGHT * GOLD_22K_PURITY,
                gram_24k_try * QUARTER_GOLD_WEIGHT * GOLD_22K_PURITY)  # QUARTER_GOLD_WEIGHT ≈ 1.75 gram 22k
    elif gold_type.lower() == "ons":
        return price_usd, price_try
    else:
        logger.error(f"❌ Bilinmeyen altın türü: {gold_type}")
        return 0.0, 0.0



