import os
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from tools.tools_registry import tools

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# _llm_instance = None
# def get_llm_instance():
#     global _llm_instance
#     if _llm_instance is None:
#         _llm_instance = create_llm().bind_tools(tools)
#     return _llm_instance


from functools import lru_cache

@lru_cache(maxsize=1)
def get_llm_instance():
    """ LLM örneğini oluşturur ve önbelleğe alır (tekil nesne gibi davranır).

    - İlk çağrıda `create_llm()` fonksiyonu çalışır ve LLM oluşturulur.
    - `bind_tools(tools)` ile tanımlı araçlar LLM'e bağlanır.
    - Sonraki çağrılarda yeniden oluşturulmaz, cache’den döner.
    - `maxsize=1` → sadece tek bir instance saklanır (singleton davranışı).
    """
    return create_llm().bind_tools(tools)


def create_llm(model: str = "openai/gpt-oss-120b", temperature: float = 0.2, max_tokens: int = 1500):
    """ ChatGroq LLM örneğini oluşturur.

    İşleyiş:
    1. `GROQ_API_KEY` ortam değişkenini alır.
    2. ChatGroq örneğini belirtilen model, temperature ve max_tokens ile oluşturur.
    3. Oluşturma sırasında bir hata olursa detaylı log atılır ve hatayı tekrar fırlatır.

    Parametreler:
        model (str): Kullanılacak LLM modeli.
        temperature (float): Yanıtların rastgelelik seviyesi.
        max_tokens (int): Maksimum token sayısı.

    Returns:
        ChatGroq: Oluşturulmuş LLM örneği.

    Raises:
        RuntimeError: API key bulunamazsa.
        Exception: LLM oluşturulurken hata oluşursa.
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY bulunamadı!")

    try:
        return ChatGroq(
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=max_tokens
        )
    except Exception as e:
        logger.error(f"LLM oluşturulurken hata: {e}")
        raise


# Kullanılabilecek diğer modeller:
# gemma2-9b-it,
# llama-3.3-70b-versatile,
# llama-3.1-8b-instant
# meta-llama/llama-guard-4-12b,
# openai/gpt-oss-120b,
# openai/gpt-oss-20b,
# whisper-large-v3

# NOT: Langchain Chatgroq yapısını kullandığım için groq hesabından desteklenen modellerden bazıları.
# Sizde kendi hesabınızdan desteklenen herhangi bir model deneyebilirsiniz ki bunlar da işinizi görecektir.
# Alternatif olarak da Hugginface' deki groq modellerini llm fonksiyonunda değişiklik yaparak kullanabilirsiniz.
