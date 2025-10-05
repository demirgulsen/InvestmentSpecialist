from ui.ui_helpers.sections import render_features_section, render_technologies_section, hero_section, render_contribute_section
from ui.ui_helpers.footer import footer_content

def show_about_page():
    """ Hakkında sayfasının bilgilerini içerir """
    hero_section(
        title="🤖 YA-DA - Yapay Zeka Destekli Yatırım Danışmanınız",
        description="<strong>Finansal geleceğinizi şekillendiren akıllı platform</strong><br>Hisse analizi, portföy optimizasyonu ve kişisel yatırım stratejileri<br>yapay zeka teknolojisiyle bir arada",
        tags=["📈 Akıllı Analiz", "🎯 Kişisel Strateji", "⚡ Gerçek Zamanlı Veriler"]
    )

    # Özellikler
    render_features_section()

    # Kullanılan Teknolojiler
    render_technologies_section()

    # Katkıda Bulunma
    render_contribute_section("Katkıda Bulunma", icon="🤝")

    # Footer
    footer_content()

