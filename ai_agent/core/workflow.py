import logging
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from ai_agent.core.state import AgentState
from tools.tools_registry import tools
from ai_agent.core.agent import agent_node

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_investment_agent():
    """ Akıllı yatırım analizi için LangGraph tabanlı AI agent'ı oluşturur ve yapılandırır.

    Returns:
        CompiledLangGraph: Derlenmiş agent workflow'u
    Workflow Akışı:
        START → agent → (tool_calls varsa) → tools → agent → END
                         (tool_calls yoksa) → END
    Node'lar:
        - agent: AI modeli ve prompt yönetimi
        - tools: Kullanılacak araçlar (hisse fiyatı, haberler, analiz)
    """

    # Workflow state graph'ini başlatır
    workflow = StateGraph(AgentState)

    # Node'lar
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", ToolNode(tools))

    # Başlangıç → agent (Her zaman agent ile başla)
    workflow.add_edge(START, "agent")

    # Agent → koşullu routing: Agent çıktısına göre yönlendirme
    workflow.add_conditional_edges(
        "agent",
        # LangGraph built-in: tool_calls varsa tools’a gider, yoksa END
        lambda state: "tools" if getattr(state["messages"][-1], "tool_calls", None) else END,
        {"tools": "tools", END: END}
    )

    # Tools → agent : Her zaman agent’a dönsün  (araç yanıtlarını işlesin)
    workflow.add_edge("tools", "agent")

    # Memory yapılandırması - konuşma hafızası için
    checkpointer = MemorySaver()

    # Workflow'u derler ve döndürür
    compiled_agent = workflow.compile(checkpointer=checkpointer)
    logger.info("✅ Yatırım agent'ı başarıyla oluşturuldu")

    return compiled_agent



