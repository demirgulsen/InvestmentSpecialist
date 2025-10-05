import pandas as pd
import streamlit as st
import logging
from config.constants import RISK_WEIGHTS, SAFETY_LEVELS
from services.asset_service import (get_currency_asset_price, get_crypto_asset_price,
                                    get_stock_asset_price, get_gold_asset_price)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_asset_values(asset, info, base_currency="TRY"):
    """ Tek bir varlığın toplam değerini hesaplar.

    Parameters:
        asset (str): Varlık adı veya sembolü.
        info (dict): Varlık bilgileri -> "amount": float, "type": str
        base_currency (str): Değerin hangi para birimi cinsinden hesaplanacağı (default: "TRY").

    Returns:
        dict: Varlığın miktarı, birim fiyatı ve toplam değeri.
    """
    try:
        amount = info["amount"]
        asset_type = info["type"]

        usd_price, try_price = get_asset_price(asset, asset_type, base_currency)
        if usd_price <= 0 or try_price <= 0:
            return {
                "Varlık": asset,
                "Miktar": "{:.2f}".format(float(amount)),
                "Fiyat (USD)": 0.0,
                "Değer (USD)": 0.0,
                "Fiyat (TRY)": 0.0,
                "Değer (TRY)": 0.0,
                "Type": asset_type,
                "Success": False,
                "Error": "Fiyat alınamadı"
            }

        usd_value = float(amount) * float(usd_price)
        try_value = float(amount) * float(try_price)
        return {
            "Varlık": asset,
            "Miktar": "{:.2f}".format(amount),
            "Fiyat (USD)": float(usd_price),
            "Değer (USD)": usd_value,
            "Fiyat (TRY)": float(try_price),
            "Değer (TRY)": try_value,
            "Type": asset_type,
            "Success": True
        }
    except Exception as e:
        logging.error(f"❌ Varlık değer hesaplama hatası ({asset}): {e}")
        return {
            "Varlık": asset,
            "Miktar": "{:.2f}".format(float(info.get("amount", 0))),
            "Fiyat (USD)": 0.0,
            "Değer (USD)": 0.0,
            "Fiyat (TRY)": 0.0,
            "Değer (TRY)": 0.0,
            "Type": info.get("type", "unknown"),
            "Success": False,
            "Error": str(e)
        }



def calculate_portfolio_values(portfolio, base_currency="TRY"):
    """ Bir portföydeki tüm varlıkların toplam değerini hesaplar.

    Parameters:
        portfolio (dict): Portföy bilgileri, örn. {"BTC": {"amount": 0.5, "type": "crypto"}, ...}
        base_currency (str): Değerin hangi para birimi cinsinden hesaplanacağı (varsayılan: "TRY").

    Return:
        tuple:
            pd.DataFrame: Varlıklar ve değerlerini içeren tablo.
            float: Portföyün toplam değeri.
    """

    results_list = []
    total_value_try = 0.0

    for asset, info in portfolio.items():
        asset = str(asset).strip()
        result = calculate_asset_values(asset, info, base_currency)
        if result["Success"]:
            result_for_df = {k: v for k, v in result.items() if k not in ["Success", "Error"]}
            results_list.append(result_for_df)
            total_value_try += float(result_for_df["Değer (TRY)"])
        else:
            st.error(f"❌ Fiyat Alınamadı: {asset} ({result['Error']})")
            logging.warning(f"Fiyat alınamadı: {asset} → {result}")

    df = pd.DataFrame(results_list)
    logging.info(f"Portföy df: {df}")

    return df, total_value_try



# get_risk_allocation -> calculate_risk_allocation
def calculate_risk_allocation(risk_selection: str, portfolio: dict) -> dict:
    """ Kullanıcının risk profiline göre önerilen dağılımı döndürür.

    Parameters:
        risk_selection: "Düşük", "Orta", "Yüksek" risk profili.
        portfolio: Kullanıcının portföyü.
            Örnek: {
                "Bitcoin": {"type": "crypto", "value": 5000},
                "AAPL": {"type": "stock", "value": 10000},
            }

    Return:
        dict: Her varlık tipine önerilen yüzdelik dağılım.
            Örnek: {"stock": 45.0, "gold": 55.0}

    Açıklama:
        - Fonksiyon, risk profiline göre "safe", "moderate", "risky" gruplarına ayrılmış
          ağırlıkları portföydeki type değerlerine uygular.
        - Kalan ağırlık, en büyük kategoriye eklenerek toplamın 100 olması sağlanır.
    """
    logger.info("portfolio: ",portfolio)

    # Kullanıcının portföyündeki kategoriler (type’lar)
    asset_categories = {info["type"] for info in portfolio.values()}

    # Seçilen risk profili
    weights = RISK_WEIGHTS.get(risk_selection, RISK_WEIGHTS["Orta"])

    allocation = {}
    remaining_weight = 100
    # Her risk grubunu portföy tiplerine dağıt
    for safety_group, weight_ratio in weights.items():
        categories_in_group = [c for c in asset_categories if SAFETY_LEVELS.get(c) == safety_group]

        if categories_in_group:
            share_per_category = (weight_ratio * 100) / len(categories_in_group)

            for cat in categories_in_group:
                allocation[cat] = round(share_per_category, 1)
                remaining_weight -= allocation[cat]

    # Kalan ağırlığı en büyük kategoriye ekle (toplam 100 olmalı)
    if remaining_weight > 0 and allocation:
        max_category = max(allocation, key=lambda x: allocation[x])
        allocation[max_category] += remaining_weight

    return allocation

    # # String formatına dönüştür
    # response_lines = [f"**{risk_selection} Risk Profili Önerileriniz:**", ""]
    # for asset_type, percentage in allocation.items():
    #     response_lines.append(f"• {asset_type.title()} → %{percentage:.1f}")
    #
    # response_lines.append("")
    # response_lines.append("Bu dağılım, risk tecihinize ve mevcut portföy yapınıza göre oluşturulmuştur.")
    #
    # return "\n".join(response_lines)



def get_asset_price(asset, asset_type, base_currency):
    """ Verilen varlığın fiyatını getirir.

    Params:
        asset (str): Fiyatı alınacak varlık adı veya sembolü.
        asset_type (str): Varlık türü ("crypto", "stock", "gold").
        base_currency (str): Fiyatın hangi para birimi üzerinden alınacağı (default: "TRY").

    Returns:
        float: Varlığın birim fiyatı base_currency cinsinden.
        None: Eğer fiyat alınamazsa.
    """
    try:
        # Döviz
        if asset_type == "currency":
            return get_currency_asset_price(asset)

        # Kripto
        elif asset_type == "crypto":
            return get_crypto_asset_price(asset)

        # Hisse
        elif asset_type == "stock":
            return get_stock_asset_price(asset)

        # Altın
        elif asset_type == "gold":
            return get_gold_asset_price(asset, base_currency)

        else:
            logger.warning(f"Bilinmeyen varlık türü: {asset_type}")
            return 0.0, 0.0

    except Exception as e:
        logger.error(f"❌ {asset_type} fiyatı alınamadı ({asset}): {e}")
        return 0.0, 0.0


# calculate_asset_values_core -> get_asset_value
def get_format_asset_value(asset, info, base_currency="TRY") -> str:
    result = calculate_asset_values(asset, info, base_currency)

    if not result["Success"]:
        return f"{result['Varlık']} için fiyat bilgisi alınamadı."

    return f"""
        {result['Varlık']} Varlık Değeri:
            • Miktar: {result['Miktar']:.2f}
            • Fiyat (USD): ${result['Fiyat (USD)']:.2f}
            • Değer (USD): ${result['Değer (USD)']:.2f}
            • Fiyat (TRY): ₺{result['Fiyat (TRY)']:.2f}
            • Değer (TRY): ₺{result['Değer (TRY)']:.2f}
            • Tip: {result['Type']}
        """.strip()
