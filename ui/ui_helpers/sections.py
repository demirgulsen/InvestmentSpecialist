import streamlit as st
from ui.ui_helpers.headers import create_about_header
from ui.ui_helpers.utils import gradient_line


def hero_section(title, description, tags):
    """ Sayfanın üst kısmındaki özet bilgileri başlık, açıklama ve etiketlerle gösterir."""

    # Sabit stil
    span_style = "background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; \
                      border-radius: 20px; font-size: 0.9rem; backdrop-filter: blur(10px);"

    # Tag HTML
    tag_html = "".join([f'<span style="{span_style}">{t}</span>' for t in tags])

    st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff655b 0%, #764ba2 100%); 
                        padding: 2rem; border-radius: 15px; margin: 1rem 0; color: white; text-align: center;
                        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);">
                 <h1 style="margin: 0; font-size: 2.5rem; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
                     {title}
                 </h1>
                 <div style="height: 3px; background: linear-gradient(90deg, #FFD700, #FF6B6B, #4ECDC4, #45B7D1); 
                             margin: 1.5rem auto; width: 60%; border-radius: 2px;"></div>
                 <p style="font-size: 1.2rem; margin: 1rem 0; opacity: 0.95; line-height: 1.6;">
                    {description}
                 </p>
                 <div style="margin-top: 2rem; display: flex; justify-content: center; flex-wrap: wrap; gap: 1rem;">
                     {tag_html}                  
                 </div>
            </div>
    """, unsafe_allow_html=True)

def render_tech_stack(header_icon: str, title:str, tech_stack:list) -> None:
    """ Teknoloji bilgilerini ve açıklamalarını gösterir.

    Params:
        title (str): Sütun başlığı
        tech_stack (list of tuples): (icon, tech_name, description)
    """
    st.markdown(f"### {header_icon}{title}")
    for icon, tech, desc in tech_stack:
        st.markdown(f"**{icon} {tech}**  \n*{desc}*")

def render_contribute_section(title, icon="🤝"):
    """ Katkıda bulunma bölümünü ekranda gösterir."""
    st.markdown("---")
    st.markdown(f"###  {icon} {title}")

    st.info("""
        **Bu proje açık kaynak ruhuyla geliştirilmiştir!**

        - 🐛 Bug raporları ve önerilerinizi paylaşın
        - 💡 Yeni özellik fikirlerinizi sunun  
        - 🔧 Kod katkılarınızla projeyi geliştirin
        - 📖 Dokümantasyonu iyileştirmemize yardım edin
        """)

def render_feature_card(feature: dict):
    """ Tek bir özellik kartını renk, ikon ve açıklama ile ekranda gösterir. """
    st.markdown(f"""
        <div style="background: white; border-left: 4px solid {feature['color']}; 
                    padding: 1.5rem; margin: 0.5rem 0; border-radius: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1); transition: transform 0.2s;">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem; margin-right: 0.5rem;">{feature['icon']}</span>
                <h3 style="color: #2c3e50; margin: 0; font-size: 1.1rem;">{feature['title']}</h3>
            </div>
            <p style="color: #7f8c8d; margin: 0; font-size: 0.9rem; line-height: 1.4;">
                {feature['desc']}
            </p>
        </div>
        """, unsafe_allow_html=True)

def get_feature_cards():
    """ Uygulamadaki tüm özellik kartlarını içeren veri listesini döndürür. """
    return [
        {
            "icon": "🏦",
            "title": "Hisse Senedi Analizi",
            "desc": "Güncel piyasa verileri ve grafiklerle detaylı analiz",
            "color": "#3498db"
        },
        {
            "icon": "💱",
            "title": "Döviz Çevirici",
            "desc": "Anlık kurlar ile kolay para birimi dönüşümü",
            "color": "#e74c3c"
        },
        {
            "icon": "📊",
            "title": "Portföy Analizi",
            "desc": "Kapsamlı portföy analizi ve akıllı risk yönetimi",
            "color": "#2ecc71"
        },
        {
            "icon": "🎯",
            "title": "Kişisel Yatırım Analizi",
            "desc": "Risk profilinize özel kişiselleştirilmiş yatırım önerileri",
            "color": "#f39c12"
        },
        {
            "icon": "🤖",
            "title": "YADA ile Sohbet",
            "desc": "Yapay zeka desteğiyle 7/24 yatırım danışmanlığı",
            "color": "#9b59b6"
        }
    ]

def render_features_section():
    """ "Uygulamanın sunduğu hizmetlerin özetini, grid layout içinde gösterir. """
    create_about_header("YADA ile Neler Yapabilirsiniz?", "🚀")
    features = get_feature_cards()

    for i in range(0, len(features), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(features):
                with cols[j]:
                    render_feature_card(features[i + j])

    # Görsel için renkli yatay çizgi
    gradient_line()

def render_technologies_section():
    """ Projede kullanılan Frontend, Backend ve AI/Entegrasyon teknolojilerini listeler."""

    create_about_header("Kullanılan Teknolojiler", "🛠️")

    col1, col2, col3 = st.columns(3)
    # --- FRONTEND ---
    with col1:
        frontend_stack = [
            ("🌐", "Streamlit", "İnteraktif web arayüzü"),
            ("📊", "Plotly & Matplotlib", "Finansal verilerin görselleştirilmesi"),
            ("🎯", "HTML/CSS", "Özel stil ve kullanıcı deneyimi")
        ]
        render_tech_stack("🎨", "Frontend", frontend_stack)

    # --- BACKEND ---
    with col2:
        backend_stack = [
            ("🐍", "Python", "Temel geliştirme dili"),
            ("📈", "yFinance", "Hisse senedi ve finansal veri çekme"),
            ("🔗", "Requests", "API veri entegrasyonu"),
            ("📊", "Pandas & NumPy", "Veri işleme ve hesaplama"),
            ("📡", "FINNHUB API", "Gerçek zamanlı piyasa verileri"),
            ("💰", "CoinGecko API", "Kripto fiyatları ve piyasa değerleri")
        ]
        render_tech_stack("⚙️", "Backend", backend_stack)

    # --- AI & ENTEGRASYON ---
    with col3:
        ai_stack = [
            ("🧠", "LangChain + Tools", "LLM için zincirleme mantık ve araç kullanımı"),
            ("📊", "LangGraph", "Agent tabanlı iş akışlarının yönetimi"),
            ("⚡", "ChatGroq", "Hızlı LLM sorguları için optimize altyapı"),
            ("🔍", "DuckDuckGo Search (DDGS)", "Web’den güncel haber ve finansal veri sorgulama")
        ]
        render_tech_stack("🤖", " Yapay Zeka & Entegrasyonlar", ai_stack)

