import logging
from langchain_core.messages import ToolMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def log_agent_response(response):
    """Agent yanıtını detaylı şekilde loglar.

    Parameter:
        response (dict): Agent çağrısından dönen yanıt.

    İşleyiş:
        1. Yanıt boşsa loglama yapmadan çıkar.
        2. Yanıt içindeki tüm key'leri loglar (debug amaçlı).
        3. Mesaj sayısını loglar.
        4. Son 5 mesajı (veya daha azsa hepsini) detaylı şekilde loglar:
            - Mesaj tipi (HumanMessage, AIMessage, ToolMessage vs.)
            - Tool çağrısı içerip içermediği
            - İçerik önizlemesi (100 karakter)
            - Eğer ToolMessage ise tool adı
    """
    if not response:
        return

    logger.info(f"Agent response keys: {list(response.keys())}")
    messages = response.get('messages', [])
    logger.info(f"Response message count: {len(messages)}")

    # En fazla 5 mesajı detaylı loglar
    recent_messages = messages[-5:] if len(messages) > 5 else messages
    for i, msg in enumerate(recent_messages):
        msg_type = type(msg).__name__
        has_tool_calls = hasattr(msg, 'tool_calls') and bool(msg.tool_calls)

        if isinstance(msg, ToolMessage):
            tool_name = getattr(msg, 'name', 'unknown')
            logger.info(f"Message {i}: {msg_type} - Tool: {tool_name}")
        else:
            content_preview = str(getattr(msg, 'content', ''))[:100]
            logger.info(
                f"Message {i}: {msg_type} - HasToolCalls: {has_tool_calls} - Content: {content_preview}...")



