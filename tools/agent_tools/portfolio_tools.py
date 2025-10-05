import logging
from langchain_core.tools import tool
from tools.tool_helpers import safe_float, format_asset_report, determine_risk_level
from tools.base_tools.calculate_portfolio_value import calculate_risk_allocation
from ai_agent.portfolio.portfolio_context_manager import portfolio_context
# from ai_agent.portfolio.portfolio_context_manager import get_portfolio_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def get_portfolio_info() -> str:
    """ Kullanıcının mevcut portföy bilgilerini getirir ve detaylı analiz sonucu verir

    Returns: Raw portfolio data (schema: PORTFOLIO_FORMAT)
    +
    💰 **PORTFÖY ÖZETİ**
    Toplam portföy özeti

    💼 **PORTFÖY ANALİZİ:**
    - Mevcut varlık dağılımı değerlendirmesi
    - Risk profili uygunluğu analizi
    - Eksik olan varlık sınıfları tespiti

    🎯 **ÖNERİLEN DAĞILIM:**
    - Hedef portföy yapısı önerisi
    - Önerilen varlık oranları
    - Alternatif yatırım araçları
    """
    try:
        # portfolio_df_info = get_portfolio_context()
        portfolio_df_info =  portfolio_context.get_portfolio_context()
        logger.info(f"portfolio info: {portfolio_df_info}")

        if not portfolio_df_info:
            return "📭 Portföy verisi bulunamadı. Lütfen önce portföyünüzü ekleyin."

        total_value_try = 0.0
        total_value_usd = 0.0
        asset_reports = []

        for asset in portfolio_df_info:
            asset_reports.append(format_asset_report(asset))
            total_value_try += safe_float(asset.get('Değer (TRY)', 0))
            total_value_usd += safe_float(asset.get('Değer (USD)', 0))

        # varlıkları birleştirir
        asset_details_str = "\n\n".join(asset_reports)

        # Genel özet
        summary = f"""
          Toplam Portföy Değeri: \n\n
          • USD: ${total_value_usd:,.2f} \n\n
          • TRY: ₺{total_value_try:,.2f} \n\n
          Toplam Varlık Sayısı: {len(portfolio_df_info)} \n\n
          VARLIK DETAYLARI: \n\n
          {asset_details_str}\n\n          
        """
        return summary

    except Exception as e:
        logger.error(f"❌ Portföy bilgisi işlenirken hata: {e}", exc_info=True)
        return f"Portföy bilgisi işlenirken hata oluştu: {str(e)}"


@tool
def get_investment_advice(risk_description: str = "orta") -> str:
    """ Kullanıcının risk tercihine göre yatırım önerisi yapar

    Parameter:
        risk_description (str): Risk seviyesi tanımı (string: "düşük", "orta", "yüksek")

    Returns: Currency conversion data (schema: CURRENCY_FORMAT)
    +
    📊 **MEVCUT PORTFÖY DAĞILIMI:**
    [Portfolio grafik varsa AYNEN göster]

    💼 **PORTFÖY ANALİZİ:**
    - Mevcut varlık dağılımı değerlendirmesi
    - Risk profili uygunluğu analizi
    - Eksik olan varlık sınıfları tespiti

    🎯 **ÖNERİLEN DAĞILIM:**
    - Hedef portföy yapısı önerisi
    - Önerilen varlık oranları
    - Alternatif yatırım araçları

    📈 **STRATEJİK ÖNERİLER:**
    - Kısa vadeli aksiyonlar (3-6 ay)

    ⚖️ **RİSK DEĞERLENDİRMESİ:**
    - {risk_description} profili uygunluğu
    - Potansiyel getiri beklentileri

    ⚠️ **YASAL UYARI:**
    Bu öneriler mevcut portföyünüz ve risk toleransınız dikkate alınarak hazırlanmıştır.
    Bu bilgiler profesyonel yatırım tavsiyesi değildir.
    """
    try:
        # portfolio_info = get_portfolio_context()
        portfolio_info = portfolio_context.get_portfolio_context()
        logger.info(f"portfolio info : {portfolio_info}")
        logger.info(f"risk description: : {risk_description}")

        if not portfolio_info:
            return "Portföy verisi bulunamadı. Lütfen önce portföyünüzü ekleyin."

        # Risk seviyesini metinden çıkar
        risk_level = determine_risk_level(risk_description)

        portfolio_values = {
            asset["Varlık"]: {**asset, "type": asset["Type"].lower()} for asset in portfolio_info
        }
        logger.info(f"portfolio values : : {portfolio_values}")

        result = calculate_risk_allocation(risk_level, portfolio_values)

        output = "MEVCUT PORTFÖY DAĞILIMI\n\n" + "─" * 50 + "\n\n"
        total = sum(result.values())

        for asset, value in result.items():
            percentage = (value / total) * 100
            bars = "█" * int(percentage // 5)
            output += f"\n\n{asset:<15} │{bars:<25}│ %{percentage:5.1f} \n\n"

        output += f"\n Toplam: ₺{total:,.0f}"
        return output

    except Exception as e:
        logger.error(f"❌ Yatırım önerisi hesaplanamadı: {e}", exc_info=True)
        return f"Yatırım önerisi hesaplanamadı: {str(e)}"

