import logging
from typing import Dict, Any, List
from langchain_core.messages import HumanMessage, BaseMessage
from datetime import datetime
from ai_agent.core.state import AgentState
from config.constants import INTEREST_KEYWORDS

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_recent_user_messages(messages: List[BaseMessage], limit: int = 5) -> List[str]:
    """ Mesaj geçmişinden son kullanıcı (HumanMessage) mesajlarını çıkarır.

    Parameters:
        messages (List[BaseMessage]): Tüm mesaj geçmişi (HumanMessage, AIMessage, SystemMessage vs.)
        limit (int, optional): Kaç adet son kullanıcı mesajının alınacağını belirler (Varsayılan = 5)

    Returns:
        List[str]: Belirlenen limit kadar son kullanıcı mesajı içerikleri.

    Örnek:
        Girdi: [H1, A1, H2, A2, H3, A3, H4] (limit=2)
        Çıktı: ["H4", "H3"]  # En yeni 2 kullanıcı mesajı

    Notlar:
        - Sadece HumanMessage tipindeki mesajları döner.
        - Boş içerikli mesajlar filtrelenir.
        - Mesaj sırası korunur, en güncel mesajlar listenin sonunda olur.
    """
    return [
        msg.content for msg in messages[-limit:]
        if isinstance(msg, HumanMessage) and msg.content
    ]

def analyze_user_interests(recent_messages: List[str]) -> List[str]:
    """ Kullanıcı mesajlarını analiz ederek ilgi alanlarını belirler.

    Parameter:
        recent_messages (List[str]): Kullanıcının son mesajları.

    Returns:
        List[str]: Kullanıcının ilgi alanı kategorileri (örn. ['döviz', 'hisse']).

    İşleyiş:
        1. Mesajları küçük harfe çevirir.
        2. INTEREST_KEYWORDS sözlüğündeki anahtar kelimeleri arar.
        3. Eşleşen kategori isimlerini (örn. 'kripto', 'altın') sonuç listesine ekler.
    """

    interests = set()
    for message in recent_messages:
        message_lower = message.lower()

        # Her kategori için anahtar kelimeleri kontrol eder
        for category, terms in INTEREST_KEYWORDS.items():
            if any(term in message_lower for term in terms):
                interests.add(category)

    return list(interests)


def update_user_context(state: AgentState, messages: List[BaseMessage]) -> Dict[str, Any]:
    """ Kullanıcı bağlamını (user_context) günceller.

    Parameters:
        state (AgentState): Mevcut workflow durumu (state).
        messages (List[BaseMessage]): Agent ile kullanıcı arasındaki tüm mesaj geçmişi.

    Returns:
        Dict[str, Any]: Güncellenmiş kullanıcı bağlamı.

    Güncellenen Alanlar:
        - recent_questions: Kullanıcının son mesajları (limitli).
        - last_interaction: Son etkileşimin zaman damgası (ISO formatında).
        - interests: Kullanıcının mesajlarına göre çıkarılan ilgi alanları.

    İşleyiş:
        1. Son kullanıcı mesajlarını alır (`get_recent_user_messages`).
        2. İlgi alanlarını analiz eder (`analyze_user_interests`).
        3. Bu bilgileri `user_context` içine yazar.
    """
    user_context = state.get('user_context', {})

    try:
        # Son kullanıcı mesajlarını analiz eder
        recent_messages = get_recent_user_messages(messages)

        if recent_messages:
            user_context.update({
                'recent_questions': recent_messages,
                'last_interaction': datetime.now().isoformat(),
                'interests': analyze_user_interests(recent_messages)
            })
            # user_context['recent_questions'] = recent_user_messages
            # user_context['last_interaction'] = datetime.now().isoformat()
            # # İlgi alanlarını çıkar (basit keyword analizi)
            # user_context['interests'] = analyze_user_interests(recent_user_messages)

    except Exception as e:
        logger.error(f"User context bilgisi güncellenemedi! Hata: {str(e)}")

    return user_context
