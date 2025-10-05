import streamlit as st
from ui.ui_helpers.headers import create_sub_header
from tools.base_tools.calculate_portfolio_value import calculate_portfolio_values
from ui.components.charts import plot_portfolio_distribution

def show_portfolio_metrics(portfolio, df, total_value: float, currency_format: str) -> None:
    """ Portföy metriklerini gösterir """

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💰 Toplam Değer", f"{total_value:,.0f} {currency_format}")
    with col2:
        st.metric("📊 Varlık Sayısı", len(portfolio))
    with col3:
        if not df.empty:
            max_asset = df.loc[df["Değer (TRY)"].idxmax(), "Varlık"]
            max_percentage = (df["Değer (TRY)"].max() / total_value) * 100
            st.metric("🎯 En Büyük Pay", f"{max_asset} ({max_percentage:.1f}%)")



def display_portfolio_summary(portfolio: dict):
    """ Portföydeki varlıkları ve miktarlarını ekranda gösterir.

    Parameter:
        portfolio (dict): Kullanıcının portföyü, format: {varlık: {"amount": float, "type": str}, ...}
    """

    if not portfolio:
        st.info("Portföyünüz boş.")
        return

    create_sub_header("Portföy Özeti", "📋")

    info_text = "\n\n".join([f"{asset}: {info['amount']}" for asset, info in portfolio.items()])
    st.info(info_text)

def display_portfolio_table(df, total_value):
    """ Portföy verilerini tablo halinde ekrana basar ve toplam değeri gösterir.

    Parameters:
        df (pd.DataFrame): Portföydeki varlıkların DataFrame'i.
        total_value (float): Portföyün toplam değeri TRY cinsinden.

    """
    cols_to_show = [col for col in df.columns if col != "Type"]
    st.table(df[cols_to_show])
    # st.table(df)
    st.success(f"💰 Toplam Portföy Değeri: {total_value:,.2f} TRY")


def get_saved_portfolio():
    """ Kaydedilen portföyü ekranda gösterir ve özet bilgiler ile dağılım grafiğini hesaplar. """

    portfolio = st.session_state.get("portfolio", {})

    if not portfolio:
        st.info("Portföyünüz boş.")
        return

    # Portföy değerlerini hesaplar
    df, total_value = calculate_portfolio_values(st.session_state["portfolio"])

    # Tabloyu ekrana basar
    display_portfolio_table(df, total_value)

    # workflow.py sayfasında kullanılacak
    st.session_state["portfolio_df_info"] = df.to_dict('records')

    # Portföy dağılım grafiğini oluşturur
    plot_portfolio_distribution(df)