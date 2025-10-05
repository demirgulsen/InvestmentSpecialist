import streamlit as st
from config.constants import GOLD_OPTIONS
from services.currency_service import get_currencies_from_api

# investment_analysis
def get_user_input() -> tuple[str, bool, str]:
    """ Kullanıcı tercihlerini alır """

    risk_selection = st.selectbox(
        "Risk Profiliniz:",
        ["Düşük", "Orta", "Yüksek"],
        help="Risk toleransınıza göre ideal dağılım önerisi alın"
    )
    show_comparison = st.checkbox("Karşılaştırma Göster", value=True)
    currency_format = st.selectbox("Para Birimi:", ["TRY", "USD", "EUR"])

    return risk_selection, show_comparison, currency_format


# portfolio_analysis
def get_currency_process():
    """ Kullanıcının döviz işlemlerini yönetir. """

    currencies = get_currencies_from_api()

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_currency = st.selectbox("Döviz seç:", ["Seçiniz"] + currencies, key="currency")
    with col2:
        amount_currency = st.number_input("Miktar",
                                          min_value=0.0,
                                          value=st.session_state.get("currency_amount", 0.0),
                                          step=1.0,
                                          key="currency_amount")

    if selected_currency != "Seçiniz" and amount_currency > 0:
        # Dropdown değişirse portföy güncellenir
        st.session_state["portfolio"][selected_currency] = {
            "amount": amount_currency,
            "type": "currency"
        }
        # st.session_state["portfolio"][selected_currency] = amount_currency
    else:
        st.session_state["portfolio"].pop(selected_currency, None)

def get_crypto_process():
    """ Kullanıcının kripto para işlemlerini yönetir. """

    # cryptos = get_available_cryptos()  # CoinGecko API'den çekilir ama yaklaşık 13.000 veri geldiği için manuel çekeceğiz

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_crypto = st.text_input(
            "Kripto Girin:",
            placeholder="Örn: Bitcoin, Ethereum, Binancecoin, Solana, Ripple",
            value="Bitcoin",
            key="crypto",
            help="Örn: Bitcoin, Ethereum, Binancecoin, Solana, Ripple Dogecoin"
        )
    with col2:
        amount_crypto = st.number_input(
            f"{selected_crypto} Miktarı",
            min_value=0.0,
            value=st.session_state.get("crypto_amount", 0.0),
            step=0.1,
            key="crypto_amount")

    if selected_crypto != "Seçiniz" and amount_crypto > 0:
        # Dropdown değişirse portföy güncellenir
        st.session_state["portfolio"][selected_crypto] = {
            "amount": amount_crypto,
            "type": "crypto"
        }
        # st.session_state["portfolio"][selected_crypto] = amount_crypto
    else:
        st.session_state["portfolio"].pop(selected_crypto, None)

def get_stock_process():
    """ Kullanıcının hisse senedi işlemlerini yönetir. """

    # stocks = get_available_stocks()  # API veya önceden belirlenmiş liste

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_stock = st.text_input(
            "Hisse Senedi Sembolü Girin:",
            placeholder="Örn: AAPL, MSFT, GOOGL, TSLA, AMZN, NVDA",
            value="AAPL",
            key="stock",
            help="Örn: AAPL, MSFT, GOOGL, TSLA, AMZN, NVDA"
        )
    with col2:
        amount_stock = st.number_input(
            f"{selected_stock} lot sayısı:",
            min_value=0.0,
            value=st.session_state.get("stock_amount", 0.0),
            step=1.0,
            key="stock_amount"
        )

    if selected_stock != "Seçiniz" and amount_stock > 0:
        st.session_state["portfolio"][selected_stock] = {
            "amount": amount_stock,
            "type": "stock"
        }
        # st.session_state["portfolio"][selected_stock] = amount_stock
    else:
        st.session_state["portfolio"].pop(selected_stock, None)

def get_gold_process():
    """ Kullanıcının altın varlıklarını yönetir. """

    col1, col2 = st.columns([2, 1])
    with col1:
        selected_gold = st.selectbox("Altın türü seç:", ["Seçiniz"] + GOLD_OPTIONS, key="gold")
    with col2:
        amount_gold = st.number_input("Miktar:",
                                      min_value=0.0,
                                      value=st.session_state.get("gold_amount", 0.0),
                                      step=0.1,
                                      key="gold_amount")
    if selected_gold != "Seçiniz" and amount_gold > 0:
        st.session_state["portfolio"][selected_gold] = {
            "amount": amount_gold,
            "type": "gold"
        }
        # st.session_state["portfolio"][selected_gold] = amount_gold
    else:
        st.session_state["portfolio"].pop(selected_gold, None)
