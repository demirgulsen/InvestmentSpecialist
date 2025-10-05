import streamlit as st
import logging
from datetime import datetime
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_agent_response(response):
    """Agent yanıtını işler ve session state'e ekler ve portföyü günceller.

    Parameter
        response: Agent'tan gelen ham yanıt dict'i
    """
    if not response:
        return

    try:
        # Assistant cevabının içeriğini çıkarır
        assistant_content = extract_assistant_response(response)
        logger.info(f"İçerik uzunluğu: {len(assistant_content)}")

        # Assistant mesajını oluşturur
        assistant_message = {
            "role": "assistant",
            "content": assistant_content,
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        # Session state'e ekler
        st.session_state.messages.append(assistant_message)

        # güncelleme işleminin gerekli olup olmadığını kondtrol et
        # if "portfolio_df_info" in response:
        #     # Portföy' ü günceller
        #     update_portfolio_from_response(response)

    except Exception as e:
        logger.error(f"Agent yanıt işleme hatası: {str(e)}")


def extract_assistant_response(agent_response: dict) -> str:
    """ Agent yanıtından assistant mesajını ya da tool mesajını alır.

    Parameter
        agent_response: Agent'tan dönen mesaj

    Returns:
     str: Assistant veya tool mesajı
    """
    try:
        response_messages = agent_response.get("messages", [])
        if not response_messages:
            return "Yanıt alınamadı."

        # Assistant yanıtını filtreler
        ai_messages = [
            m for m in response_messages
            if isinstance(m, AIMessage) and not getattr(m, "tool_calls", None)
        ]
        if ai_messages:
            logger.info(f"Agent messages: {ai_messages[-1].content.strip()}")
            return f"{ai_messages[-1].content.strip()}"

        # Tool yanıtını filtreler
        tool_messages = [
            m for m in response_messages if isinstance(m, ToolMessage)
        ]
        if tool_messages:
            logger.info(f"Tool messages: {tool_messages[-1].content.strip()}")
            return f"{tool_messages[-1].content.strip()}"
        return "Sistem geçici olarak yanıt veremiyor."

    except Exception as e:
        logger.error(f"Yanıt işlenme hatası: {str(e)}")
        return "Yanıt işlenirken bir hata oluştu."


def update_portfolio_from_response(response):
    """Agent yanıtından portföy verilerini günceller.

    Parameter
        response: Agent invoke metodundan dönen yanıt dict'i

    Güncelleme Koşulları:
        - Response geçerli olmalı
        - updated_portfolio mevcut olmalı
        - Mevcut portföyden farklı olmalı
    """
    try:
        # Güncellenmiş portföy verisini al
        updated_portfolio = response.get("portfolio_df_info", [])

        if updated_portfolio and updated_portfolio != st.session_state.get("portfolio_df_info", []):
            st.session_state.portfolio_df_info = updated_portfolio
            logger.info(f"Portfolio güncellendi: {len(updated_portfolio)} items")

    except Exception as e:
        logger.error(f"❌ Portföy güncelleme hatası: {str(e)}")
