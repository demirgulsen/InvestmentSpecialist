import streamlit as st
from ui.ui_helpers.headers import create_main_header, create_sub_header
from ui.handlers.currency_converter_input_handler import handle_convert_button
from ui.components.currency_components import render_currency_input, display_exchange_rates


def show_currency_converter_page():
    """ Döviz çevirme işlemlerini yönetir """

    create_main_header("Döviz Çevirici", "💱")

    # Kullanıcıdan çevrilecek miktar ve para birimlerini alır
    amount, from_currency, to_currency = render_currency_input()

    # Döviz çevirme işlemlerini yapar ve sonucu ekranda gösterir
    if st.button("Çevir"):
        handle_convert_button(amount, from_currency, to_currency)

    st.markdown("---")
    create_sub_header("Güncel Döviz Kurları", "📊")

    # Anlık döviz kurlarını ekranda listeler
    display_exchange_rates()

