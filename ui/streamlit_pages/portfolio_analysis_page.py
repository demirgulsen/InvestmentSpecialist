import streamlit as st
from ui.components.portfolio_components import get_saved_portfolio
from ui.ui_helpers.headers import create_main_header, create_sub_header
from ui.components.inputs import get_currency_process, get_crypto_process, get_stock_process, get_gold_process


def show_portfolio_analysis_page():
    """ Portföy analizi yapar

    İşlevler:
    - Kullanıcıdan varlık türlerini ve miktar bilgilerini alır.
    - Portföy verilerini session state'e kaydeder.
    - Kaydedilen portföyün tablo ve grafik ile özetini gösterir.
    """

    create_main_header("Portföy Analizi", "📊")

    # Session'da portfolio key'i yoksa oluşturur
    if "portfolio" not in st.session_state:
        st.session_state["portfolio"] = {}

    with st.form("portfolio_form"):
        st.write("💡 Varlıklarını seç ve miktarını gir:")

        # --- Döviz ---
        create_sub_header("Döviz", "💱")
        get_currency_process()

        # --- Kripto ---
        create_sub_header("Kripto", "🪙")
        get_crypto_process()

        # --- Hisse ---
        create_sub_header("Hisse Senedi", "📈")
        get_stock_process()

        # --- Altın ---
        create_sub_header("Altın", "🥇")
        get_gold_process()

        submitted = st.form_submit_button("📌 Portföyü Kaydet")
        if submitted:
            st.success("✅ Portföy kaydedildi!")

    # Kaydedilen portföyü tablo ve grafik olarak göster
    get_saved_portfolio()
