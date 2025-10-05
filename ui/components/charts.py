import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib.figure import Figure
from ui.ui_helpers.headers import create_sub_header
from api_clients.stock_client import get_7day_stock_history
from api_clients.currency_clients import convert_ids_to_currency_with_exchange, current_exchange_rates, fetch_day7_currency_data


def create_pie_chart(df, values_col, names_col, title):
    """Verilen DataFrame'den pasta grafiği (pie chart) oluşturur.

    Parameters:
        df (pd.DataFrame): Veri kaynağı (portföy dağılımı).
        values_col (str): Değerleri temsil eden sütun adı (ör. "Değer (TRY)").
        names_col (str): Dilim isimlerini temsil eden sütun adı (ör. "Varlık").
        title (str): Grafiğin başlığı.
    Return:
        plotly.graph_objects.Figure: Hazır pasta grafiği objesi.
    """
    fig = px.pie(
        df,
        values=values_col,
        names=names_col,
        title=title,
        color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Değer: %{value:,.0f} TRY<br>Oran: %{percent}<extra></extra>'
    )

    fig.update_layout(
        showlegend=True,
        height=400,
        font=dict(size=12)
    )

    return fig


def create_portfolio_pie_chart(df) -> Figure:
    """ Portföydeki varlıkların değer dağılımını gösteren pasta grafiği oluşturur.

    Parameter:
        df (pd.DataFrame): Portföy bilgilerini içeren dataframe.
    Return:
        matplotlib.figure.Figure: Pasta grafiği.
    """
    fig, ax = plt.subplots(figsize=(5, 5), dpi=120)
    wedges, texts, autotexts = ax.pie(
        df["Değer (TRY)"],
        labels=df["Varlık"],
        autopct=lambda p: f'{p:.1f}%\n({p / 100 * df["Değer (TRY)"].sum():,.0f} TRY)',
        startangle=90,
        colors=plt.get_cmap("tab20").colors,
        textprops={"fontsize": 8}
    )
    ax.axis("equal")  # Daire şeklinde gösterir

    # Legend ekler ( grafiğin renkleri ile veri etiketlerini eşleştiren açıklama kutusu.)
    ax.legend(wedges, df["Varlık"], title="Varlıklar", loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1), fontsize=7)

    return fig


def plot_portfolio_distribution(df):
    """ Portföy dağılımını pasta grafiği ile gösterir.

    Parameter:
        df: Portföy bilgilerini içeren dataframe.
    """

    if not df.empty and df["Değer (TRY)"].sum() > 0:
        create_sub_header("Portföy Dağılımı (TRY Cinsinden)", "📊")

        fig = create_portfolio_pie_chart(df)
        st.pyplot(fig, clear_figure=True, use_container_width=False)
    else:
        st.info("📌 Grafik için yeterli veri yok.")


def plot_day_stock(result):
    """ Seçilen hisse senedinin gün içi fiyat hareketlerini görselleştirir.

     Parameter:
        result (dict): Hisse senedi verilerini içeren sözlük.
     """

    # Günlük veri grafiği
    fig = go.Figure()

    # Candlestick benzeri gösterim
    fig.add_trace(go.Scatter(
        x=['Açılış', 'Düşük', 'Yüksek', 'Güncel'],
        y=[result['open'], result['low'], result['high'], result['current_price']],
        mode='lines+markers',
        name=f"{result['ticker']} Fiyat",
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=8)
    ))

    fig.update_layout(
        title=f"{result['ticker']} Gün İçi Fiyat Hareketi",
        xaxis_title="Zaman",
        yaxis_title="Fiyat ($)",
        height=400,
        showlegend=True,
        template="plotly_white"
    )

    st.plotly_chart(fig, use_container_width=True)


def plot_7day_stock(stock_symbol):
    """ Seçilen hisse senedinin son 7 gündeki kapanış fiyatlarını çizer ve toplam değişim yüzdesini gösterir.

    Parameter:
        stock_symbol (str): Hisse senedi sembolü
    Return:
        plotly.graph_objs.Figure: 7 günlük kapanış fiyat grafiği
    """
    df = get_7day_stock_history(stock_symbol)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df['Close'],
        mode='lines+markers',
        name=f'{stock_symbol} Kapanış Fiyatı',
        line=dict(color='#1f77b4', width=3),
        marker=dict(size=6)
    ))

    fig.update_layout(
        title=f'{stock_symbol} Son 7 Gün Kapanış Fiyatı',
        xaxis_title='Tarih',
        yaxis_title='Fiyat (USD)',
        template='plotly_white',
        height=400
    )

    change_7d = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
    st.metric("7 Günlük Değişim", f"{change_7d:+.2f}%")

    return fig


def plot_day7_currency(from_currency: str, to_currency: str):
    """ Çapraz kur verilerini kullanarak 7 günlük fiyat grafiğini çizer.

    Parameters
        from_currency : str
            Kaynak para birimi
        to_currency : str
            Hedef para birimi
    Return
        plotly.graph_objects.Figure
            7 günlük çapraz kuru gösteren çizgi grafiği.
    """
    df = fetch_day7_currency_data(from_currency, to_currency)

    fig = px.line(
        df, x="date", y="rate",
        title=f"{from_currency.upper()} → {to_currency.upper()} (7 Günlük)"
    )
    return fig