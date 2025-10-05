import logging
from langchain_core.messages import SystemMessage, AIMessage
from ai_agent.core.llm import get_llm_instance
from ai_agent.utils.prompts import SystemPrompt
from ai_agent.core.state import AgentState
from config.constants import MAX_HISTORY
from ai_agent.utils.context_manager import update_user_context
from ai_agent.portfolio.portfolio_context_manager import portfolio_context
# from ai_agent.portfolio.portfolio_context_manager import set_portfolio_context

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def trim_messages(messages: list) -> list:
    """ Mesaj geçmişini optimize eder: SystemMessage'ları korur, son mesajları sınırlar.

    Parameter:
        messages: İşlenecek mesaj listesi (HumanMessage, AIMessage, SystemMessage, vb.)

    Returns:
        List[BaseMessage]: Optimize edilmiş mesaj listesi

    Strateji:
        1. Tüm SystemMessage'ları koru
        2. Son MAX_HISTORY kadar mesajı al (performans için)
        3. SystemMessage'ları başa, recent mesajları sona ekle

    Örnek:
        Girdi: [S1, H1, A1, H2, A2, H3, A3, H4, A4] (MAX_HISTORY=4)
        Çıktı: [S1, H3, A3, H4, A4]
    """
    if not messages:
        return []

    system_msgs = [msg for msg in messages if isinstance(msg, SystemMessage)]
    recent_msgs = messages[-MAX_HISTORY:]
    return system_msgs + recent_msgs


def agent_node(state: AgentState) -> AgentState:
    """Agent düğümü: LLM çağırır, state'i günceller ve sonraki adıma hazırlar.

    Parameter:
        state: Mevcut agent durumu (messages, portfolio, context)

    Returns:
        AgentState: Güncellenmiş agent durumu

    İşlem Akışı:
        1. Bağımlılık yükler
        2. Portföy context'ini ayarlar
        3. System prompt kontrolü ve ekleme işlemi yapar
        4. Mesajları optimize eder (trim)
        5. LLM çağrısı yapar
        6. Kullanıcı context'ini günceller
        7. Güncellenmiş state'i döndürür
    """
    try:
        # Bağımlılıkları yükler
        llm = get_llm_instance()

        # State'den verileri alır
        portfolio_df_info = state.get('portfolio_df_info', [])
        messages = state.get("messages", [])

        # Portföy bilgisini global context'e aktarır
        # set_portfolio_context(portfolio_df_info)
        logger.info(f"portfolio info: {portfolio_df_info}")
        portfolio_context.set_portfolio_context(portfolio_df_info)

        # Mesajları system prompt' a ekler
        if not any(isinstance(msg, SystemMessage) for msg in messages):
            messages.insert(0, SystemMessage(content=SystemPrompt.MAIN_SYSTEM_PROMPT))

        # Mesajları kırpar
        trimmed_messages = trim_messages(messages)

        # LLM çağrısı yapar
        response = llm.invoke(trimmed_messages)

        # User context' i günceller
        user_context = update_user_context(state, trimmed_messages)

        # Yeni state oluşturur ve döndürür
        return {
            **state,
            "messages": trimmed_messages  + [response],
            "user_context": user_context,
            "portfolio_df_info": portfolio_df_info,
        }

    except Exception as e:
        logger.error(f"Agent node hatası: {str(e)}")

        # Hata mesajını assistant cevabı gibi ekleyelim
        error_message = AIMessage(content="❌ Sistem geçici bir hata nedeniyle yanıt veremedi.")
        return {
            **state,
            "messages": state.get("messages", []) + [error_message],
            "user_context": state.get("user_context"),
            "portfolio_df_info": state.get("portfolio_df_info"),
        }
