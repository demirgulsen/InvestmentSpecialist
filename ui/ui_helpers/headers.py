import streamlit as st

def create_main_header(title: str, icon: str) -> None:
    """ Ana sayfa başlığı oluşturur """
    render_gradient_header(title, icon, font_size="2rem")

def create_about_header(title: str, icon: str = "📋") -> None:
    """ Hakkında sayfası başlığı oluşturur """
    render_gradient_header(title, icon, font_size="1.5rem")

def create_sub_header(title: str, icon: str = "📋") -> None:
    """ Alt Başlık oluşturur """

    st.markdown(f"""
        <div style="background: white; padding: 1rem; border-radius: 6px; box-shadow: 0 2px 4px rgba(44, 62, 80, 0.1); margin: 1rem 0;">
            <h3 style="color: #2c3e50; margin: 0; font-size: 1.1rem;">
                {icon} {title}
            </h3>
        </div>
    """, unsafe_allow_html=True)

def render_gradient_header(title: str, icon: str, font_size: str) -> None:
    """ Gradient arkaplan ile başlığı gösterir. """
    st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    padding: 2rem; border-radius: 12px; margin: 1.5rem 0;">
            <h1 style="color: #2c3e50; text-align: left; font-size: {font_size};">
                {icon} {title}
            </h1>
        </div>
    """, unsafe_allow_html=True)