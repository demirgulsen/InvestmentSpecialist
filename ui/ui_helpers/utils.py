import streamlit as st

def gradient_line():
    """ Sayfada görsel bir ayrım için renkli yatay bir çizgi (gradient line) ekler. """

    st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <div style="height: 2px; background: linear-gradient(90deg, #3498db, #e74c3c, #2ecc71, #f39c12, #9b59b6); 
                        margin: 0 auto; width: 60%; border-radius: 1px;"></div>
        </div>
        """, unsafe_allow_html=True)

