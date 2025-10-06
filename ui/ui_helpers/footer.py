import streamlit as st

def footer_content() -> None:
    """ Sayfanın alt kısmında gösterilecek footer içeriğini gösterir. """
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: #f8f9fa; 
                    border-radius: 10px; margin-top: 2rem;">
            <h4>🤖 YA-DA - Yapay Zeka Destekli Yatırım Danışmanınız</h4>
            <p style="color: #666; margin: 0;">
                Modern teknolojilerle geliştirilmiş, kullanıcı dostu finans aracı
            </p>
            <p style="color: #999; font-size: 0.9rem; margin-top: 1rem;">
                Geliştirici: © 2025 alpyula.coder - Gülşen Demir              
            </p>    
        </div>
        """, unsafe_allow_html=True)
