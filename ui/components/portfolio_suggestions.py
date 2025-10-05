import streamlit as st

def get_portfolio_categories(portfolio: dict) -> set:
    """ Portföydeki varlıkların kategorilerini döndürür.

    Parameter:
        portfolio: Kullanıcı portföyü
    Return:
        set: Portföydeki benzersiz varlık türleri.
    """
    return {info["type"] for info in portfolio.values()}

def get_missing_categories(risk_allocations: dict, portfolio: dict) -> set:
    """ Risk dağılımında olup portföyde eksik olan kategorileri getirir.

    Parameters:
        risk_allocations: Risk profilinin önerdiği dağılım yüzdeleri.
        portfolio: Kullanıcının mevcut portföyü.
    Return:
        set: Portföyde olmayan ve önerilen kategoriler.
    """
    portfolio_categories = get_portfolio_categories(portfolio)
    return set(risk_allocations.keys()) - set(portfolio_categories)

def suggest_missing_assets(risk_allocations: dict, portfolio: dict) -> None:
    """ Eksik varlık sınıfları için öneri üretir.

    Parameters:
        risk_allocations: Risk profilinin önerdiği dağılım yüzdeleri.
        portfolio: Kullanıcının mevcut portföyü.
    """
    missing_assets = get_missing_categories(risk_allocations, portfolio)
    if missing_assets:
        st.subheader("📈 Portföyünüzü Güçlendirebilecek Varlıklar")
        for asset in missing_assets:
            suggested_amount = risk_allocations[asset]
            st.info(
                f"💡 {asset} varlık sınıfını portföyünüze eklemek "
                f"portföy dengenizi iyileştirebilir (%{suggested_amount:.1f} önerilen)"
            )

def generate_suggestions(current_df, recommended_values, total_value):
    """ Portföy önerileri oluşturur.

     Parameters:
        current_df (DataFrame): Portföy  tablosu.
        recommended_values (dict): Her varlık türü için önerilen toplam değer.
        total_value (float): Portföyün toplam değeri.
    Return:
        list[str]: Maksimum 3 öneri.
    """
    suggestions = []
    for asset_type, recommended_val in recommended_values.items():
        matched_assets = current_df[current_df["Type"] == asset_type]
        for _, row in matched_assets.iterrows():
            current_val = row["Değer (TRY)"]
            difference = recommended_val - current_val
            asset_name = row["Varlık"]
            if abs(difference) > total_value * 0.1:  # %10 eşiği
                if difference > 0:
                    suggestions.append(f"💰 {asset_name} varlığınızı ~{difference:,.0f} TRY artırın.")
                else:
                    suggestions.append(f"📉 {asset_name} varlığınızı ~{abs(difference):,.0f} TRY azaltın.")
    if not suggestions:
        suggestions.append("🎉 Portföyünüz risk profilinize uygun dengede!")

    return suggestions[:3]  # En fazla 3 öneri göstersin

def show_investment_suggestions(df, portfolio, recommended_values, risk_allocations, total_value) -> None:
    """ Yatırım önerileri ve eksik varlıkları gösterir.

    Parameters:
        df (pd.DataFrame): Portföy tablosu
        portfolio (dict): Kullanıcının mevcut portföyü
        recommended_values (dict): Her varlık türü için önerilen toplam değer (TRY).
        risk_allocations (dict): Kullanıcının risk profilinin önerdiği varlık dağılımları (%).
        total_value (float): Portföyün toplam değeri (TRY).
    """

    # Yatırım önerileri
    st.subheader("💡 Yatırım Önerileri")
    suggestions = generate_suggestions(df, recommended_values, total_value)
    for suggestion in suggestions:
        st.info(suggestion)

    # Eksik varlık önerileri
    if len(risk_allocations) > len(portfolio):
        st.subheader("📈 Portföyünüzü Güçlendirebilecek Varlıklar")
        suggest_missing_assets(risk_allocations, portfolio)

