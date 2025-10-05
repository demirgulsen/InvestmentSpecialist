import logging
import streamlit as st
from datetime import datetime
from services.agent_service import invoke_agent
from services.response_processing import handle_agent_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def handle_agent_input() -> None:
    """ Kullanıcı sorusunu alır ve sorunun işlenmesi için process_user_query fonksiyonuna gönderir. """

    user_input = st.chat_input("💬 Sorunuzu yazın:", key="user_input")

    logger.info(f"Portfolio: {st.session_state.get('portfolio_df_info', [])}")

    if not user_input:
        return

    # Çıkış komutları kontrolü
    if user_input.lower() in ['q', 'quit', 'exit', 'çıkış']:
        st.warning("👋 Sohbet sonlandırıldı. İyi günler!")
        st.stop()

    # Kullanıcı sorusunu işler
    process_user_question(user_input)


def process_user_question(question: str):
    """ Kullanıcı sorusunu işler ve agent yanıtını yönetir.
        1. session_state’e ekler
        2. agent’i çağırır
        3. yanıtı session_state’e kaydeder

    Parameter:
        question: Kullanıcı sorusu
    """
    try:
        # Kullanıcı mesajını session'a ekler
        add_user_message(question)

        # Agent'tan yanıt alır
        with st.spinner("🤔 Düşünüyorum..."):
            response = invoke_agent(question)

        # Yanıtı işler ve session'a kaydeder
        handle_agent_response(response)

    except Exception as e:
        logger.error(f"Soru işlenirken hata oluştu: {str(e)}")

        error_message = {
            "role": "assistant",
            "content": f"❌ Üzgünüm, bir hata oluştu. Lütfen tekrar deneyin.",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.messages.append(error_message)
    st.rerun()


def add_user_message(question: str):
    """ Kullanıcı mesajını session state'e ekler.

    Parameter:
        question: Kullanıcı sorusu

    Session State Structure:
        messages: List[dict]
        - role: "user" | "assistant"
        - content: mesaj içeriği
        - timestamp: "HH:MM:SS" formatında zaman damgası
    """
    user_message = {
        "role": "user",
        "content": question,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    st.session_state.messages.append(user_message)
