import streamlit as st
from config.constants import CURRENCY_SYMBOLS, CURRENCY_VALUES
from ui.components.charts import plot_day7_currency
from services.currency_service import get_current_exchange_rates


def get_plot_7day_currency(from_currency, to_currency):
    """ Son 7 güne ait döviz kuru hareketlerini görselleştirir.

    Parameters:
        from_currency (str): Kaynak para birimi (örn. "USD").
        to_currency (str): Hedef para birimi (örn. "TRY").
    """
    fig = plot_day7_currency(from_currency, to_currency)
    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("❌ Grafik verisi alınamadı.")



def display_exchange_rates():
    """ Güncel döviz kurlarını ekranda gösterir.

    İşlev:
        - get_current_exchange_rates fonksiyonundan kur verilerini alır.
        - Her bir döviz kuru için stilize edilmiş bir kutu (card) oluşturur.
        - 4’erli kolonlar halinde Streamlit sayfasında grid layout ile gösterir.
    """
    rates = get_current_exchange_rates()
    if not rates:
        st.error("❌ Kur bilgisi alınamadı.")
        return

    # 4’erli gruplar halinde kolon oluştur
    items = list(rates.items())
    n = 4
    for i in range(0, len(items), n):
        cols = st.columns(n)
        for j, (currency, rate) in enumerate(items[i:i + n]):
            with cols[j]:
                st.markdown(
                    f"""
                    <div style="background-color:#3f5372; padding:20px; border-radius:15px; text-align:center; color:white; margin-bottom:10px;">
                        <h3>{CURRENCY_SYMBOLS[currency]['symbol']} {currency}</h3>
                        <p style="font-size:16px;">{CURRENCY_SYMBOLS[currency]['name']}</p>
                        <p style="font-size:24px;">₺{rate:.2f}</p>
                    </div>
                    """, unsafe_allow_html=True)


def render_currency_input():
    """ Kullanıcıdan kaynak ve hedef para birimi ile miktarı alır."""

    col1, col2, col3 = st.columns(3)
    with col1:
        from_currency = st.selectbox("Kaynak Para Birimi", CURRENCY_VALUES)
    with col2:
        to_currency = st.selectbox("Hedef Para Birimi", CURRENCY_VALUES)
    with col3:
        amount = st.number_input("Miktar", min_value=1.0, value=100.0)

    return amount, from_currency, to_currency
