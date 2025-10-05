""" portfolio_tools fonksiyonlarının yardımcı fonksiyonlarını içerir. """

def safe_float(value) -> float:
    """Her türlü string/int/None değerini float'a çevirir.

    Parameter:
         value: Float’a çevrilmek istenen değer (str, int, None vb.)
    Returns:
        float: Geçerli float değeri, hatalıysa 0.0 döner
    """
    try:
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return float(value)
    except (ValueError, TypeError, AttributeError):
        return 0.0


def format_asset_report(asset: dict) -> str:
    """ Tek bir varlık için detaylı portföy raporu oluşturur.

    Parameter:
        asset (dict): Portföydeki tek bir varlık bilgisi

    Returns:
        str: Formatlanmış varlık raporu
    """
    asset_name = asset.get('Varlık', 'Unknown')
    asset_type = asset.get('Type', 'bilinmiyor')
    amount = safe_float(asset.get('Miktar', 0))
    price_usd = safe_float(asset.get('Fiyat (USD)', 0))
    value_usd = safe_float(asset.get('Değer (USD)', 0))
    price_try = safe_float(asset.get('Fiyat (TRY)', 0))
    value_try = safe_float(asset.get('Değer (TRY)', 0))

    return (
        f"{asset_name} ({asset_type}):\n"
        f"  • Miktar: {amount:,.2f}\n"
        f"  • Birim Fiyat (USD): ${price_usd:,.2f}\n"
        f"  • Toplam Değer (USD): ${value_usd:,.2f}\n"
        f"  • Birim Fiyat (TRY): ₺{price_try:,.2f}\n"
        f"  • Toplam Değer (TRY): ₺{value_try:,.2f}\n"
    )


def determine_risk_level(risk_description: str) -> str:
    """Risk seviyesini metin bazlı analiz ederek 'Düşük', 'Orta', 'Yüksek' olarak döner.

    Parameter:
        risk_description (str): Risk tercihini açıklayan string
    Returns:
        str: Risk seviyesi ('Düşük', 'Orta', 'Yüksek')
    """
    text = risk_description.lower()
    if any(word in text for word in ['düşük', 'güvenli', 'az']):
        return "Düşük"
    elif any(word in text for word in ['yüksek', 'agresif', 'riskli']):
        return "Yüksek"
    return "Orta"