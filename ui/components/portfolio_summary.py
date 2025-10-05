import streamlit as st
from ui.components.charts import create_portfolio_pie_chart
from ui.ui_helpers.headers import create_sub_header
from tools.base_tools.calculate_portfolio_value import calculate_portfolio_values


def render_portfolio_table(df):
    """Portföy tablosunu gösterir."""
    if df is not None and not df.empty:
        cols_to_show = [col for col in df.columns if col != "Type"]
        st.table(df[cols_to_show])
    else:
        st.info("📌 Portföy tablosu için veri yok.")

def render_portfolio_total(total_value):
    """Toplam portföy değerini gösterir."""
    st.success(f"💰 Toplam Portföy Değeri: {total_value:,.2f} TRY")

def render_portfolio_pie_chart(df):
    """Portföy dağılım grafiğini gösterir."""
    if not df.empty and df["Değer (TRY)"].sum() > 0:
        fig = create_portfolio_pie_chart(df)
        st.pyplot(fig, clear_figure=True, use_container_width=False)
    else:
        st.info("📌 Grafik için yeterli veri yok.")

def summer_portfolio(portfolio):
    """ Portföy özetini gösterir: tablo + grafik + toplam değer """
    create_sub_header("Portföy Özeti")

    # Veri Hesaplama ve Görselleştirme
    try:
        df, total_value_try = calculate_portfolio_values(portfolio)  # Bu fonksiyon önceden tanımlı olmalı

        render_portfolio_table(df)

        render_portfolio_total(total_value_try)

        create_sub_header("Portföy Dağılımı (TRY Cinsinden)", "📊")

        # Dağılım grafiği
        render_portfolio_pie_chart(df)

    except Exception as e:
        st.error(f"Hata oluştu: {e}")