import pandas as pd
import streamlit as st
import plotly.express as px
from ui.components.charts import create_pie_chart
from tools.base_tools.comparison_table import create_comparison_table


def show_comparison_charts(comparison_df: pd.DataFrame, risk_selection: str) -> None:
    """ Mevcut ve önerilen portföy karşılaştırma grafiklerini getirir """

    if comparison_df.empty:
        st.warning("Karşılaştırma yapılacak veri bulunamadı.")
        return

    # Tüm varlıklar için sabit renk paleti oluştur
    unique_assets = comparison_df["Varlık"].unique()
    colors = px.colors.qualitative.Set1[:len(unique_assets)]
    color_map = dict(zip(unique_assets, colors))

    col1, col2 = st.columns(2)

    # Mevcut portföy grafiği
    with col1:
        st.subheader("📊 Mevcut Portföy")
        # Mevcut değerleri float olarak al
        df_plot = comparison_df.copy()
        df_plot["Mevcut (TRY)"] = df_plot["Mevcut (TRY)"].str.replace(",", "").astype(float)
        fig1 = create_pie_chart(df_plot, "Mevcut (TRY)", "Varlık", "Mevcut Portföy")
        fig1.update_traces(marker_colors=[color_map[asset] for asset in df_plot["Varlık"]])
        st.plotly_chart(fig1, use_container_width=True)

    # Önerilen portföy grafiği
    with col2:
        st.subheader("🎯 Önerilen Dağılım")
        df_plot = comparison_df.copy()
        df_plot["Önerilen (TRY)"] = df_plot["Önerilen (TRY)"].str.replace(",", "").astype(float)
        fig2 = create_pie_chart(df_plot, "Önerilen (TRY)", "Varlık", f"{risk_selection} Risk Profili")
        fig2.update_traces(marker_colors=[color_map[asset] for asset in df_plot["Varlık"]])
        st.plotly_chart(fig2, use_container_width=True)


def render_comparison_table_and_charts(df, recommended_values, total_value, show_comparison, risk_selection):
    """Portföy vs önerilen dağılım tablosu ve grafiklerini gösterir."""
    comparison_df = None
    if show_comparison and not df.empty:
        comparison_df = create_comparison_table(df, recommended_values, total_value)
        st.subheader("📋 Portföy vs Önerilen Dağılım")
        st.dataframe(comparison_df, use_container_width=True)

        # Karşılaştırma grafikleri
        show_comparison_charts(comparison_df, risk_selection)
