import streamlit as st
import logging
import uuid
from ai_agent.core.workflow import create_investment_agent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_chat_state() -> None:
    """ Session state değişkenlerini başlatır ve agent'ı hazırlar.
        - messages: Kullanıcı ve agent arasındaki konuşmaları tutar.
        - thread_id: Her oturum için benzersiz kimlik oluşturur.
        - agent: create_investment_agent ile oluşturulan yatırım agent instance'ı.
        - portfolio_df_info: Portföy bilgilerini saklar.
    """

    # Chat mesaj geçmişi - kullanıcı ve AI yanıtlarını içerir
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Her konuşma için benzersiz ID - agent memory izolasyonu sağlar
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    # AI agent instance'ı - yatırım analizi işlemlerini yönetir
    if "agent" not in st.session_state:
        st.session_state.agent = create_investment_agent()

    # Portföy bilgilerini saklar
    if "portfolio_df_info" not in st.session_state:
        st.session_state.portfolio_df_info = []


def get_agent_config():
    """ Agent için thread bazlı konfigürasyon nesnesi oluşturur.

     Returns:
         - configurable.thread_id: Session state üzerinde oluşturulan eşsiz thread_id
         - Örnek: {"configurable": {"thread_id": "uuid-string"}}
     """
    return {"configurable": {"thread_id": st.session_state.thread_id}}


def get_current_state():
    """ Agent'in mevcut durumunu döndürür.

    Returns:
        AgentState veya None: Agent'ın mevcut durum bilgisi
     """
    config = get_agent_config()
    last_state = st.session_state.agent.get_state(config)
    logger.info(f"Thread ID: {st.session_state.thread_id}")
    logger.info(f"Last state exists: {bool(last_state)}")
    return last_state if last_state else None