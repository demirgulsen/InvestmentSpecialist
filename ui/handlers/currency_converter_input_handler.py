import streamlit as st
from services.currency_service import get_exchange_currency
from ui.components.currency_components import render_currency_input, get_plot_7day_currency, display_exchange_rates


def handle_convert_button(amount, from_currency, to_currency):
    """ Döviz çevirme işlemini gerçekleştirir ve 7 günlük döviz kuru grafiğini ekranda gösterir

    Parameters:
        amount (float): Çevrilecek miktar
        from_currency (str): Kaynak para birimi (örn. "USD")
        to_currency (str): Hedef para birimi (örn. "TRY")
    """

    with st.spinner("Çevriliyor..."):
        conversion_result = get_exchange_currency(amount, from_currency, to_currency)
        if conversion_result["success"]:
            st.success(f"💱 {conversion_result.get("result")}")

            # --- 7 Günlük fiyat grafiği ---
            get_plot_7day_currency(from_currency, to_currency)
        else:
            st.error("❌ Kur bilgisi alınamadı.")
