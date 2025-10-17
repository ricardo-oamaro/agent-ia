# 📰 Market News Monitor

Um projeto fullstack (FastAPI + React + Tailwind) que monitora **notícias de empresas** em tempo real usando **Google News RSS** e **IA para classificação de eventos**.

---

## 🚀 Visão Geral

O **Market News Monitor** coleta automaticamente notícias de empresas e classifica cada uma em:
- Aquisição  
- Certificação  
- Lançamento de Produto  
- Outro  

O frontend exibe as notícias com **filtros de eventos**, layout moderno em **Tailwind**, e links clicáveis direto para a fonte.

---

## 🧩 Stack

| Camada | Tecnologia |
|--------|-------------|
| **Backend** | [FastAPI](https://fastapi.tiangolo.com/) + [Uvicorn](https://www.uvicorn.org/) |
| **Frontend** | [React](https://react.dev/) + [Vite](https://vitejs.dev/) + [TailwindCSS](https://tailwindcss.com/) |
| **Parser** | [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) |
| **IA (opcional)** | OpenAI API (`OPENAI_API_KEY`) |
| **Origem das notícias** | Google News RSS (`https://news.google.com/rss/search`) |

---

## 🧠 Funcionalidades

✅ Busca automática de notícias (Google News RSS)  
✅ IA (opcional) para classificar e resumir notícias  
✅ Filtros por tipo de evento  
✅ Card clicável com redirecionamento direto ao artigo  
✅ Interface responsiva e moderna (Tailwind)  
✅ Backend com CORS liberado para o frontend local  

---

## ⚙️ Como rodar localmente

### 🔹 Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
