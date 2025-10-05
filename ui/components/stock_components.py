import streamlit as st
from ui.components.charts import plot_day_stock, plot_7day_stock


def get_stock_info(result):
    """ Hisse senedine ait fiyat bilgilerini gösterir """
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Güncel Fiyat", f"${result['current_price']:.2f}")

    with col2:
        st.metric(
            "Değişim",
            f"${result['change']:.2f}",
            f"{result['change_percent']:.2f}%"
        )

    with col3:
        st.metric("Açılış", f"${result['open']:.2f}")

    with col4:
        st.metric("Gün İçi", f"${result['low']:.2f} - ${result['high']:.2f}")

def get_analysis_summer(result):
    """ Hisse senedinin günlük performans özetini gösterir """

    change_color = "green" if result['change'] >= 0 else "red"
    change_emoji = "📈" if result['change'] >= 0 else "📉"

    st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px;">
            <h4>{change_emoji} Günlük Performans</h4>
            <p style="color: {change_color}; font-size: 18px; font-weight: bold;">
            {result['change']:+.2f} USD ({result['change_percent']:+.2f}%)
            </p>
            <p><strong>Değerlendirme:</strong> 
            {"Pozitif trend 🚀" if result['change'] >= 0 else "Negatif trend ⚠️"}
            </p>
        </div>
    """, unsafe_allow_html=True)


def get_select_stock():
    """ Hisse seçim işlemlerini yapar """
    col1, col2 = st.columns([3, 1])

    with col1:
        stock_symbol = st.text_input(
            "Hisse Senedi Sembolü Girin:",
            placeholder="Örn: AAPL, MSFT, GOOGL, TSLA",
            value="AAPL"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_button = st.button("📊 Analiz Et", type="primary")

    st.info("💡 **İpucu:** Popüler hisse sembolleri: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA")

    return stock_symbol, analyze_button


def render_stock_info(result):
    """ Hisse bilgilerini ve analiz özetini gösterir. """
    st.markdown("### 📊 Hisse Bilgileri")
    get_stock_info(result)

    # *** Grafikleri ekle ***
    st.markdown("---")
    st.markdown("### 📈 Günlük Fiyat Grafiği")
    plot_day_stock(result)

    st.markdown("---")
    st.markdown("### 📈 Son 7 Günlük Fiyat Grafiği")
    fig = plot_7day_stock(result['ticker'])
    st.plotly_chart(fig, use_container_width=True)

    # Ek bilgiler
    st.markdown("---")
    st.markdown("### 💡 Analiz Özeti")
    get_analysis_summer(result)