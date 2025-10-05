# 🤖 YA-DA  - Yatırım Danışmanı Asistanı

---

## 🧠 Hakkında

YA-DA, modern yatırımcılar için tasarlanmış LLM tabanlı bir portföy yönetim ve yatırım danışmanlığı asistanıdır.
Kullanıcılarla doğal dilde etkileşime girer, portföyünüzü analiz eder, risk seviyenizi değerlendirir ve size özel yatırım stratejileri sunar.
> ⚠️ **Not:** Bu bir portföy projesidir


## 🚀 Özellikler

| Emoji | Özellik | Açıklama |
|-------|---------|----------|
| 💬 | Akıllı Chatbot | LangChain + ChatGroq destekli doğal dil etkileşimi |
| 💰 | Portföy Analizi | Gerçek zamanlı varlık değerleme, dağılım ve getiri hesaplama |
| 📈 | Hisse & Döviz Verileri | Finnhub, CoinGecko ve yFinance entegrasyonları |
| 🧩 | AI Workflow | LangGraph tabanlı dinamik tool routing |
| 🧮 | Risk Analizi & Öneriler | Kullanıcının risk profilini çıkarır, uygun yatırım dağılımı önerir |
| 🔍 | Güncel Veri Araması | DDGS (DuckDuckGo) ile web’den canlı finansal haber sorgulama |
| 🌐 | Streamlit UI | Etkileşimli web arayüzü ve görselleştirmeler (Plotly & Matplotlib) |


## 🧩 Mimarisi
Streamlit UI ──> LangGraph Agent ──> ChatGroq LLM
      │                  │              │
      ▼                  ▼              ▼
  Grafikler &       State & Memory   API / Tools
  Kullanıcı Girişi  Yönetimi         (Finnhub, CoinGecko, DDGS)


## 🧰 Kullanılan Teknolojiler

### 🎨 Frontend
- 🌐 Streamlit — Etkileşimli arayüz
- 📊 Plotly & Matplotlib — Finansal grafikler
- 🎯 HTML / CSS — UI özelleştirmeleri

### ⚙️ Backend
- 🐍 Python — Ana geliştirme dili
- 📡 Finnhub API — Gerçek zamanlı piyasa verisi
- 💰 CoinGecko API — Kripto fiyatları
- 📈 yFinance — Hisse senedi verisi
- 🔗 Requests — API entegrasyonu
- 📊 Pandas & NumPy — Veri işleme

### 🤖 AI & Entegrasyon
- 🧠 LangChain + Tools — LLM tool entegrasyonu
- 📊 LangGraph — Agent akış yönetimi
- ⚡ ChatGroq — Hızlı LLM 
- 🔍 DDGS — Web üzerinden güncel bilgi arama

## 🧑‍💻 Geliştirici
👋 Gülşen Demir — Jr. Data Scientist & AI Developer

## 📫 İletişim: 
LinkedIn : [https://linkedin.com/in/gulsendemir](https://www.linkedin.com/in/gulsendemir/)
GitHub : [https://github.com/demirgulsen/]
Kaggle : [https://www.kaggle.com/gulsendemir]
