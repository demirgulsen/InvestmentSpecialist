from tools.agent_tools.financial_tools import convert_currency_for_exchange
from tools.agent_tools.financial_tools import get_stock_data
from tools.agent_tools.portfolio_tools import get_investment_advice
from tools.agent_tools.portfolio_tools import get_portfolio_info
from tools.agent_tools.search_tools import search_duckduckgo

# LLM'in kullanabileceği araçlar (tools)
tools = [
    search_duckduckgo,              # Web arama yapar
    convert_currency_for_exchange,  # Döviz veya para birimi dönüşümü gerçekleştirir
    get_stock_data,                 # Hisse senedi ve finansal veri sağlar
    get_portfolio_info,             # Kullanıcının portföy bilgilerini döner
    get_investment_advice           # Yatırım tavsiyesi ve öneriler üretir
]



