import streamlit as st
import logging
import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def system_infos() -> None:
    """ Sistemin mevcut durum bilgilerini genişletilebilir panelde gösterir.

    Gösterilen Bilgiler:
    - Thread/Session ID
    - Mesaj istatistikleri
    - Portföy durumu
    - Sistem zamanı
    """
    st.divider()
    with st.expander("ℹ️ Sistem Bilgileri"):
        st.write(f"🆔 Thread ID: `{st.session_state.thread_id[:8]}...`")
        st.write(f"💬 Toplam Mesaj: {len(st.session_state.messages)}")
        st.write(f"⏰ Son Güncelleme: {datetime.datetime.now().strftime('%H:%M:%S')}")

        try:
            portfolio_df_info = st.session_state.get('portfolio_df_info', [])
            if isinstance(portfolio_df_info, list) and len(portfolio_df_info) > 0:
                portfolio_count = len(st.session_state.get('portfolio_df_info', []))
                status = "✅ Aktif" if portfolio_count > 0 else "❌ Boş"
                st.write(f"📊 Portföy Durumu: {status} ({portfolio_count} varlık)")
            else:
                st.write("📊 Portföy Durumu: ❌ Boş")

        except Exception as e:
            st.write("📊 Portföy Durumu: ❓ Bilinmiyor")
            logger.error(f"Portfolio info access error: {str(e)}")