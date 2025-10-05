from typing import TypedDict, Annotated, Optional, Dict, Any, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    Agent ile ilgili oturum (session) durumunu tanımlar.

    Fields:
        messages (List[BaseMessage]):
            - Mesaj geçmişi (otomatik olarak birleştirilir - LangGraph tarafından otomatik olarak yönetilir.)
        portfolio_df_info (Optional[List[Dict[str, Any]]]):
            - Portföy bilgilerini içeren dict yapısı.
        user_context (Optional[Dict[str, Any]]):
            - Kullanıcı tercihleri ve oturum bilgileri

    Annotated Kullanımı:
        - messages: add_messages fonksiyonu ile otomatik mesaj birleştirme
    """
    messages: Annotated[List[BaseMessage], add_messages]
    portfolio_df_info: Optional[List[Dict[str, Any]]]
    user_context: Optional[Dict[str, Any]]
