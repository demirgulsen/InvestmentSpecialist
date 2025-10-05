# ENG
## 🤖 YA-DA - Investment Specialist Assistant

### 🧠 About

YA-DA is an LLM-powered investment **specialist assistant** designed for investors.  
It interacts with users in natural language, analyzes portfolios, evaluates risk levels, and provides insights to support informed investment decisions.  
> ⚠️ **Note:** This is a portfolio project. It does not provide real investment advice.

### 🚀 Features

|       | Feature | Description |
|-------|---------|-------------|
| 💬 | Smart Chatbot | Natural language interaction powered by LangChain + ChatGroq |
| 💰 | Portfolio Analysis | Real-time asset valuation, distribution, and returns calculation |
| 📈 | Stock & Currency Data | Integration with Finnhub, CoinGecko, and yFinance |
| 🧩 | AI Workflow | Dynamic tool routing powered by LangGraph |
| 🧮 | Risk Analysis & Recommendations | Detects user risk profile and suggests suitable investment allocation |
| 🔍 | Live Data Search | DDGS (DuckDuckGo) for up-to-date financial news |
| 🌐 | Streamlit UI | Interactive web interface and visualizations (Plotly & Matplotlib) |

### 🧩 Architecture

| Technology | Responsibility |
|------------|----------------|
| 🌐 **Streamlit UI**  ➡️ | Graphs & User Input |
| 🤖 **LangGraph Agent** ➡️ | State & Memory Management |
| ⚡ **ChatGroq LLM**  ➡️ | API / Tools (Finnhub, CoinGecko, DDGS) |

### 🧰 Tech Stack

#### 🎨 Frontend
- 🌐 Streamlit — Interactive UI
- 📊 Plotly & Matplotlib — Financial visualizations
- 🎯 HTML / CSS — UI customizations

#### ⚙️ Backend
- 🐍 Python — Core programming language
- 📡 Finnhub API — Real-time market data
- 💰 CoinGecko API — Cryptocurrency prices
- 📈 yFinance — Stock market data
- 🔗 Requests — API integration
- 📊 Pandas & NumPy — Data processing

#### 🤖 AI & Integration
- 🧠 LangChain + Tools — LLM tool integration
- 📊 LangGraph — Agent workflow management
- ⚡ ChatGroq — High-speed LLM
- 🔍 DDGS — Web-based live information retrieval

**Note:**
Initially, I worked with the 'gemma2-9b-it' model. This model was particularly valuable due to its fast results and for understanding prompt design and tool logic. However, I used 'openai/gpt-oss-120b' for this project as I had reached my usage quota.

Other models that can be used in this project:
- gemma2-9b-it
- llama-3.3-70b-versatile
- llama-3.1-8b-instant
- meta-llama/llama-guard-4-12b
- openai/gpt-oss-120b
- openai/gpt-oss-20b
- whisper-large-v3

Additionally:
- Since this project uses the LangChain + ChatGroq structure, you can choose any model supported by your Groq account.
- You can also experiment with other supported models from your own account; most will work fine.
- Alternatively, HuggingFace Groq models can be used by modifying the llm function accordingly.

### 🧑‍💻 Developer
👋 **Gülşen Demir** — Jr. Data Scientist & AI Developer

### 📫 Contact
- Youtube: 
- LinkedIn: [linkedin.com/in/gulsendemir](https://www.linkedin.com/in/gulsendemir/)  
- GitHub: [github.com/demirgulsen](https://github.com/demirgulsen/)  
- Kaggle: [kaggle.com/gulsendemir](https://www.kaggle.com/gulsendemir)


---

# TR
## 🤖 YA-DA  - Yatırım Danışmanı Asistanı


### 🧠 Hakkında

YA-DA, yatırımcılar için tasarlanmış LLM tabanlı bir portföy yönetim ve yatırım danışmanlığı asistanıdır.
Kullanıcılarla doğal dilde etkileşime girer, portföyünüzü analiz eder, risk seviyenizi değerlendirir ve size özel yatırım stratejileri sunar.
> ⚠️ **Not:** Bu bir portföy projesidir. Gerçek yatırım tavsiyesi sunmaz!


### 🚀 Özellikler

|       | Özellik | Açıklama |
|-------|---------|----------|
| 💬 | Akıllı Chatbot | LangChain + ChatGroq destekli doğal dil etkileşimi |
| 💰 | Portföy Analizi | Gerçek zamanlı varlık değerleme, dağılım ve getiri hesaplama |
| 📈 | Hisse & Döviz Verileri | Finnhub, CoinGecko ve yFinance entegrasyonları |
| 🧩 | AI Workflow | LangGraph tabanlı dinamik tool routing |
| 🧮 | Risk Analizi & Öneriler | Kullanıcının risk profilini çıkarır, uygun yatırım dağılımı önerir |
| 🔍 | Güncel Veri Araması | DDGS (DuckDuckGo) ile web’den canlı finansal haber sorgulama |
| 🌐 | Streamlit UI | Etkileşimli web arayüzü ve görselleştirmeler (Plotly & Matplotlib) |


### 🧩 Mimarisi

| Teknoloji | Görev |
|-----------|-------|
| 🌐 **Streamlit UI**  ➡️| Grafikler & Kullanıcı Girişi |
| 🤖 **LangGraph Agent** ➡️| State & Memory Yönetimi |
| ⚡ **ChatGroq LLM**  ➡️| API / Tools (Finnhub, CoinGecko, DDGS) |


### 🧰 Kullanılan Teknolojiler

#### 🎨 Frontend
- 🌐 Streamlit — Etkileşimli arayüz
- 📊 Plotly & Matplotlib — Finansal grafikler
- 🎯 HTML / CSS — UI özelleştirmeleri

#### ⚙️ Backend
- 🐍 Python — Ana geliştirme dili
- 📡 Finnhub API — Gerçek zamanlı piyasa verisi
- 💰 CoinGecko API — Kripto fiyatları
- 📈 yFinance — Hisse senedi verisi
- 🔗 Requests — API entegrasyonu
- 📊 Pandas & NumPy — Veri işleme

#### 🤖 AI & Entegrasyon
- 🧠 LangChain + Tools — LLM tool entegrasyonu
- 📊 LangGraph — Agent akış yönetimi
- ⚡ ChatGroq — Hızlı LLM 
- 🔍 DDGS — Web üzerinden güncel bilgi arama

**Not:**
Projede başlangıçta 'gemma2-9b-it' modeli ile çalıştım.Bu model, sonuçları hızlı getirmesi ve prompt ile tool mantığını anlamak açısından oldukça değerliydi fakat istek kotamı doldurduğum için 'openai/gpt-oss-120b' modelini kullandım. 

Ayrıca projede kullanılabilecek diğer modeller:
- gemma2-9b-it,
- llama-3.3-70b-versatile,
- llama-3.1-8b-instant
- meta-llama/llama-guard-4-12b,
- openai/gpt-oss-120b,
- openai/gpt-oss-20b,
- whisper-large-v3

Ek olarak:
- LangChain + ChatGroq yapısını kullandığım için Groq hesabınızda desteklenen modellerden herhangi birini seçebilirsiniz.
- Kendi hesabınız üzerinden desteklenen farklı modelleri deneyebilirsiniz; çoğu işinizi görecektir.
- Alternatif olarak, HuggingFace üzerindeki Groq modellerini llm fonksiyonunda değişiklik yaparak kullanabilirsiniz.


### 🧑‍💻 Geliştirici
👋 **Gülşen Demir** — Jr. Data Scientist & AI Developer

### **📫 İletişim:**
- Youtube: 
- LinkedIn: [linkedin.com/in/gulsendemir](https://www.linkedin.com/in/gulsendemir/)  
- GitHub: [github.com/demirgulsen](https://github.com/demirgulsen/)  
- Kaggle: [kaggle.com/gulsendemir](https://www.kaggle.com/gulsendemir)  
