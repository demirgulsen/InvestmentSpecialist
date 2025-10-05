import streamlit as st
from tools.base_tools.calculate_portfolio_value import calculate_portfolio_values
from tools.base_tools.calculate_portfolio_value import calculate_risk_allocation
from ui.components.portfolio_summary import summer_portfolio
from ui.components.portfolio_components import show_portfolio_metrics
from ui.components.portfolio_comparison import render_comparison_table_and_charts
from ui.components.portfolio_suggestions import show_investment_suggestions
from ui.ui_helpers.headers import create_main_header, create_sub_header
from ui.components.inputs import get_user_input


def show_investment_analysis_page():
    """ Yatırım analizi sayfası - tüm bileşenleri yönetir """
    create_main_header("Kişisel Yatırım Analizi", "💼")

    # Session kontrolü
    if "portfolio" not in st.session_state or not st.session_state["portfolio"]:
        st.info("📌 Önce portföy sayfasından portföyünüzü kaydedin.")
        return

    portfolio = st.session_state["portfolio"]

    # --- Portföy Özeti ---
    summer_portfolio(portfolio)

    # --- Kişisel Yatırım Analizi ---
    create_sub_header("Kişisel Yatırım Analizi", "🎯")

    # Kullanıcı tercihlerini alır
    risk_selection, show_comparison, currency_format = get_user_input()

    try:
        #  Veri hazırlama
        df, total_value = calculate_portfolio_values(st.session_state["portfolio"])

        # Metrikleri gösterme
        show_portfolio_metrics(portfolio, df, total_value, currency_format)

        # Risk profili dağılımı
        risk_allocations = calculate_risk_allocation(risk_selection, portfolio)
        recommended_values = {asset_type: total_value * pct / 100 for asset_type, pct in risk_allocations.items()}

        # Karşılaştırma tablosu
        render_comparison_table_and_charts(df, recommended_values, total_value, show_comparison, risk_selection)

        # Öneriler
        if show_comparison and not df.empty:
            show_investment_suggestions(df, portfolio, recommended_values, risk_allocations, total_value)

    except Exception as e:
        st.error(f"❌ Analiz hatası: {e}")
