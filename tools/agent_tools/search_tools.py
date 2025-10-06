from ddgs import DDGS
from langchain_core.tools import tool

@tool
def search_duckduckgo(query: str) -> str:
    """ DuckDuckGo arama aracı - güncel bilgiler için web araması yapar.

    Parameter:
        query: Aranacak sorgu (string)

    Returns: Raw conversion data (use SEARCH_FORMAT)
    +
    🔍 ARAMA SONUÇLARI:
    - İlgili başlıklar ve özetler
    - Güncel bilgi kaynakları
    - Web sitesi linkleri
    """
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=5)

            if not results:
                return "Sonuç alınamadı"

            formatted_results = []
            for i, result in enumerate(results, 1):
                formatted_results.append(f"{i}. {result['title']}\n{result['body'][:200]}...\n")

            return "\n".join(formatted_results)

    except Exception as e:
        return f"Arama yapılamadı. Hata: {str(e)}"
