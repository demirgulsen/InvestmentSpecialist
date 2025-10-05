import streamlit as st
from ui.streamlit_pages.about_page import show_about_page
from ui.streamlit_pages.chatbot_page import show_chatbot_page
from ui.streamlit_pages.portfolio_analysis_page import show_portfolio_analysis_page
from ui.streamlit_pages.currency_converter_page import show_currency_converter_page
from ui.streamlit_pages.stock_analysis_page import show_stock_analysis_page
from ui.streamlit_pages.investment_analysis_page import show_investment_analysis_page


# Streamlit page config
st.set_page_config(
    page_title="YA-DA - Yatırım Danışmanınız",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ile özelleştirme
st.markdown("""
    <style>
    /* Sidebar arka plan rengi */
    [data-testid="stSidebar"] {
        background-color: #102950; /* istediğin hex kodunu yaz */
    }
    
    /* Sidebar başlık ve metin rengi */
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p {
        color: white;
    }

    /* Sidebar buton stilleri */
    [data-testid="stSidebar"] button {
        width: 200px !important;   /* sabit genişlik */
        height: 50px !important;   /* sabit yükseklik */
        margin: 5px 0px;           /* aralık */
        font-size: 16px !important;
        font-weight: bold;
        text-align: left !important;
        border-radius: 10px;
        justify-content: flex-start !important; /* ikonu varsa sola dayar */
        background-color: #FF3F33 !important;  /* Canlı Turuncu */
        color: white !important;
        border: none !important;
    }
    
    /* Hover efekti */
    [data-testid="stSidebar"] button:hover {
        background-color: #cc3228 !important; /* Hover koyu mavi ton */
        cursor: pointer;
    }   
    
    .stButton > button:focus {
        background-color: #F0F2F6;
        color: #262730;
        border: 1px solid #FF4B4B;
        outline: none;
        box-shadow: 0 0 0 2px rgba(255, 75, 75, 0.2);
    }
    
    </style>
    """, unsafe_allow_html=True)


# Durum Bilgisi - Proje Çalıştırıldığında İlk Açılacak Sayfa
if "page" not in st.session_state:
    st.session_state.page = "Hakkında"

def go_to(page_name):
    st.session_state.page = page_name


# --- Proje Tanıtımı ---
st.sidebar.markdown(
    """
    <div style="background-color: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: #FFFFFF; text-align: center; margin-bottom: 10px;">🚀 YA-DA Hakkında</h3>
        <p style="color: #FFFFFF; font-size: 14px; line-height: 1.5;">
            <strong>Y</strong>apay zeka destekli<br>
            <strong>Y</strong>atırım <strong>D</strong>anışmanı <strong>A</strong>sistanı
        </p>
        <ul style="color: #FFFFFF; font-size: 12px; margin: 10px 0;">
            <li>📈 Hisse senedi analizi</li>
            <li>🔴 Gerçek zamanlı piyasa verileri</li>
            <li>📊 Portföy analizi</li>
            <li>🎯 Kişiselleştirilmiş yatırım analizi</li>
            <li>⚖️ Risk değerlendirmesi</li>
            <li>🤖 YA-DA chat ile akıllı finansal rehberlik</li>
        </ul>
        <h3 style="color: #FFD700; font-size: 15px; text-align: center; margin-top: 5px;">
            ⚠️ Bu bir DEMO projesidir - Gerçek yatırım tavsiyesi içermez!
        </h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")


# --- Sidebar Menü ---
st.sidebar.markdown("Hangi işlemi yapmak istersiniz?")

if st.sidebar.button("ℹ️ Proje Hakkında.."):
    go_to("Hakkında")

if st.sidebar.button("🏦 Hisse Senedi Analizi"):
    go_to("Hisse Senedi Analizi")

if st.sidebar.button("💱 Döviz Çevirici"):
    go_to("Döviz Çevirici")

if st.sidebar.button("📊 Portföy Analizi"):
    go_to("Portföy Analizi")

if st.sidebar.button("🎯 Kişisel Yatırım Analizi"):
    go_to("Kişisel Yatırım Analizi")

if st.sidebar.button("🤖 YA-DA ile Sohbet Edin"):
    go_to("YA-DA ile Sohbet Edin")

# --- Sayfalar ---
if st.session_state.page == "Hakkında":
    show_about_page()

elif st.session_state.page == "Hisse Senedi Analizi":
    show_stock_analysis_page()

elif st.session_state.page == "Döviz Çevirici":
    show_currency_converter_page()

elif st.session_state.page == "Portföy Analizi":
    show_portfolio_analysis_page()

elif st.session_state.page == "Kişisel Yatırım Analizi":
    show_investment_analysis_page()

elif st.session_state.page == "YA-DA ile Sohbet Edin":
    show_chatbot_page()

############################################################################
# if 'current_context' not in st.session_state:
#     st.session_state.current_context = {}

# Durum çubukları
# status_col1, status_col2 = st.columns(2)

# session_state durumları tanımlanmalı
# Örneğin: site, selected_restaurant, selected_product, chart ... gibi

# with status_col1:
#     if st.session_state.current_context.get("site"):
#         st.success(f"🌐 Hisse Senedi Analizi: {st.session_state.current_context.get("site").title()}")
#
# with status_col2:
#     if st.session_state.current_context.get("selected_restaurant"):
#         st.success(f"🏪 Kişisel Yatırım Analizi: {st.session_state.current_context.get("selected_restaurant").title()}")
#
