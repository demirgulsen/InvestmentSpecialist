import pandas as pd

def create_comparison_table(current_df, recommended_values, total_value):
    """ Mevcut portföy ile önerilen portföy dağılımını karşılaştıran tabloyu oluşturur.

    Parameters:
        current_df (pd.DataFrame): Kullanıcının mevcut portföy verisi.
        recommended_values (dict): Önerilen portföy dağılımı.
            - Örn: {"hisse": 5000, "döviz": 3000, "altın": 2000}
        total_value (float): Toplam portföy değeri (TRY).
    Return:
        pd.DataFrame: Karşılaştırma tablosu.
    """

    # Mevcut portföy verilerini düzenler
    comparison_data = []
    for _, row in current_df.iterrows():
        asset_type = row["Type"]
        if asset_type in recommended_values:  # sadece önerilen kategorilere bak
            current_val = row["Değer (TRY)"]
            recommended_val = recommended_values[asset_type]
            difference = current_val - recommended_val

            comparison_data.append({
                "Varlık": row["Varlık"],
                "Mevcut (TRY)": f"{current_val:,.0f}",
                "Mevcut (%)": f"{(current_val / total_value) * 100:.1f}%",
                "Önerilen (TRY)": f"{recommended_val:,.0f}",
                "Önerilen (%)": f"{(recommended_val / total_value) * 100:.1f}%",
                "Fark": f"{difference:+,.0f}",
                "Durum": "✅ Uygun" if abs(difference) < total_value * 0.05
                else ("🔴 Az" if difference < 0 else "🟡 Fazla")
            })

    return pd.DataFrame(comparison_data)
