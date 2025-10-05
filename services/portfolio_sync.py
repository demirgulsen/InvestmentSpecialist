import streamlit as st
import logging
from ai_agent.portfolio.portfolio_context_manager import portfolio_context
# from ai_agent.portfolio.portfolio_context_manager import set_portfolio_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sync_portfolio_with_state(last_state):
    """Agent state içindeki portföy ile session state içindeki portföyü senkronize eder.

    Amaç:
        - Kullanıcının portföy bilgisi hem agent'ın belleğinde (state)
          hem de Streamlit session_state içinde tutuluyor.
        - Bu fonksiyon, ikisini karşılaştırarak en güncel olanı seçer
          ve tüm sisteme yayar.

    Parameter:
        last_state (AgentState | None):
            Agent'ın son state bilgisi.

    Returns:
        list[dict]: Güncel portföy verisi (her bir varlığı temsil eden dict listesi).

    İşleyiş:
        1. Eğer session_state içinde portföy varsa, öncelikli olarak o alınır.
        2. Aksi halde agent state içindeki portföy kullanılır.
        3. Güncel portföy Streamlit session_state ve portfolio context içine yazılır.
        4. Senkronize edilen portföy geri döndürülür.
    """
    memory_portfolio = last_state.values.get('portfolio_df_info', []) if last_state else []
    session_portfolio = st.session_state.get('portfolio_df_info', [])

    # En güncel portfolio'yu belirler
    current_portfolio = session_portfolio if session_portfolio else memory_portfolio

    if current_portfolio:
        st.session_state.portfolio_df_info = current_portfolio

        # set_portfolio_context(current_portfolio)
        portfolio_context.set_portfolio_context(current_portfolio)
        logger.info(f"Güncel portfolio bilgisi ayarlandı, varlık sayısı: {len(current_portfolio)}")

    return current_portfolio
