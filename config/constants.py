"""
Bu dosya proje boyunca kullanılan sabit değerleri içermektedir.
"""

# calculate_portfolio_value.py
GRAM_PER_OUNCE = 31.1034768
GOLD_22K_PURITY = 0.916
QUARTER_GOLD_WEIGHT = 1.75


# agent.py
MAX_HISTORY = 20


# calculate_portfolio_value
MAPPING_GOLD = {
    "Gram Altın (22k)": "gram-22",
    "Gram Altın (24k)": "gram-24",
    "Çeyrek Altın": "ceyrek",
    "ONS Altın": "ons"
}

# context_manager.py
INTEREST_KEYWORDS = {
        'döviz': ['dolar', 'euro', 'tl', 'kur', 'usd', 'eur', 'try', 'exchange'],
        'hisse': ['hisse', 'senedi', 'stock', 'borsa', 'şirket'],
        'portföy': ['portföy', 'yatırım', 'varlık', 'portfolio', 'investment'],
        'altın': ['altın', 'gold', 'gram', 'ceyrek'],
        'kripto': ['bitcoin', 'ethereum', 'kripto', 'btc', 'eth', 'crypto'],
        'risk': ['risk', 'riskli', 'güvenli', 'konservatif', 'agresif']
    }


# core_tools.calculate_risk_allocation
# Risk profiline göre temel dağılımlar (yüzde)  -> “rule of thumb” (kural bazlı) dağılımlar
RISK_WEIGHTS = {
    "Düşük": {"safe": 0.7, "moderate": 0.25, "risky": 0.05},
    "Orta": {"safe": 0.4, "moderate": 0.45, "risky": 0.15},
    "Yüksek": {"safe": 0.15, "moderate": 0.35, "risky": 0.5},
}

# Proje type → risk grubu eşleştirmesi
SAFETY_LEVELS = {
    "gold": "safe",  # Altın
    "currency": "moderate",  # Döviz
    "stock": "moderate",  # Hisse
    "crypto": "risky"  # Kripto
}

# core_tools.get_available_currencies_core
SYMBOLS = ["USD", "EUR", "TRY", "GBP", "CHF", "JPY", "CAD", "KRW","QAR", "AED", "RUB", "UAH", "CNY"]

# streamlit_pages.portfolio_analysis_pae
GOLD_OPTIONS = ["Gram Altın (22k)", "Gram Altın (24k)", "Çeyrek Altın", "ONS Altın"]


# currency_components.py
CURRENCY_SYMBOLS = {
    "USD": {"symbol": "$", "name": "Amerikan Doları"},
    "EUR": {"symbol": "€", "name": "Euro"},
    "GBP": {"symbol": "£", "name": "İngiliz Sterlini"},
    "CHF": {"symbol": "₣", "name": "İsviçre Frangı"},
    "JPY": {"symbol": "¥", "name": "Japon Yeni"},
    "CAD": {"symbol": "C$", "name": "Kanada Doları"},
    "KRW": {"symbol": "₩", "name": "Güney Kore Wonu"},
    "QAR": {"symbol": "ر.ق", "name": "Katar Riyali"},
    "AED": {"symbol": "د.إ", "name": "BAE Dirhemi"},
    "RUB": {"symbol": "₽", "name": "Rus Rublesi"},
    "UAH": {"symbol": "₴", "name": "Ukrayna Grivnası"},
    "CNY": {"symbol": "¥", "name": "Çin Yuanı"}
}

CURRENCY_VALUES = ["USD", "EUR", "TRY", "GBP", "CHF", "JPY", "CAD", "KRW", "QAR", "AED", "RUB", "UAH", "CNY"]

