import streamlit as st
import logging
from langchain_core.messages import HumanMessage
from services.session_manager import get_current_state, get_agent_config
from services.portfolio_sync import sync_portfolio_with_state
from ui.handlers.log_handler import log_agent_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def prepare_agent_input(question: str, last_state, current_portfolio) -> dict:
    """ Agent için input nesnesini hazırlar.

    Parameters:
        question (str): Kullanıcı sorusu.
        last_state: Workflow'un son bilinen state objesi (AgentState).
        current_portfolio: Kullanıcının güncel portföy bilgileri (list yapısı).

    Returns:
        dict: Agent'e gönderilecek input nesnesi. Şu alanları içerir:
            - messages (List[HumanMessage]): Yeni kullanıcı sorusu.
            - portfolio_df_info (Any): Güncel portföy verisi.
            - user_context (dict): Kullanıcıya ait son bilinen bağlam (Son soruları, son etkileşim zamanı, ilgi alanları).

    İşleyiş:
        1. Yeni gelen soruyu `HumanMessage` içine sarar.
        2. Mevcut portföy bilgilerini ekler.
        3. Son state varsa içinden `user_context` bilgisini çıkarır.
        """

    agent_input = {
        "messages": [HumanMessage(content=question)],
        "portfolio_df_info": current_portfolio,
        "user_context": last_state.values.get('user_context', {}) if last_state else {}
    }
    return agent_input


def invoke_agent(question: str):
    """ Kullanıcıdan gelen soruyu işleyip Agent'a iletir, yanıtı döner.

    Parameter:
        question (str): Kullanıcının sorusu / isteği.
    Returns:
        dict: Agent tarafından üretilen yanıt.
              İçinde "messages" ve güncel state bilgileri bulunur.
    """

    # Son state bilgilerini alır
    last_state = get_current_state()

    # Portföy bilgisini state ile senkronize eder
    current_portfolio = sync_portfolio_with_state(last_state)

    # Agent için gerekli input'u hazırlar
    agent_input = prepare_agent_input(question, last_state, current_portfolio)
    config = get_agent_config()
    logger.info(f"Sending to agent: {question}")

    # Agent'ı verilen config ile çağırır
    response = st.session_state.agent.invoke(agent_input, config=config)

    # Gelen yanıtı detaylı şekilde loglar (log_agent_messages).
    log_agent_response(response)

    return response




