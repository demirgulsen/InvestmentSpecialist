import streamlit as st
from services.stock_services import get_stock_data_core
from ui.ui_helpers.headers import create_main_header
from ui.components.stock_components import get_select_stock, render_stock_info
# from tools.market_api import get_stock_data


def show_stock_analysis_page():
    """ Hisse senedi analizi yapar """
    create_main_header("Hisse Senedi Analizi", "📈")

    # Hisse senedi seçimi
    stock_symbol, analyze_button = get_select_stock()

    # Analiz sonuçlarını görüntüler
    st.markdown("---")
    if analyze_button and stock_symbol:
        with st.spinner(f"{stock_symbol.upper()} analiz ediliyor..."):
            try:
                result = get_stock_data_core(stock_symbol.upper())
                if result.get("success"):
                    st.success("✅ Analiz tamamlandı!")
                    render_stock_info(result)
                else:
                    st.error("❌ Veri alınamadı. Lütfen tekrar deneyin.")

            except Exception as e:
                st.error(f"❌ Hata oluştu: {str(e)}")
