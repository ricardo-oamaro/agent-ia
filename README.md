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
| **Parser** | [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) + [lxml](https://lxml.de/) |
| **HTTP Client** | [httpx](https://www.python-httpx.org/) (async/sync) |
| **IA (opcional)** | OpenAI API (`OPENAI_API_KEY`) |
| **Fontes de dados** | 9 fontes (Google News, G1, InfoMoney, UOL, Reuters, Yahoo, DuckDuckGo, LinkedIn, Bing) |

---

## 🧠 Funcionalidades

✅ Busca automática em **10 fontes diferentes** de notícias  
✅ **🏢 NOVO:** Busca direta no **site oficial da empresa** (Nubank, Totvs, Stone, etc)  
✅ **📅 NOVO:** Notícias **ordenadas por data** (mais recentes primeiro)  
✅ **🕒 NOVO:** Filtro temporal - apenas notícias dos **últimos 7 dias**  
✅ **Fontes Brasileiras**: Google News, G1 Globo, InfoMoney, UOL Economia  
✅ **Fontes Internacionais**: Reuters, Yahoo Finance, DuckDuckGo, Bing News, LinkedIn  
✅ IA (opcional) para classificar e resumir notícias  
✅ Filtros por tipo de evento e empresa  
✅ Cards clicáveis com redirecionamento direto ao artigo  
✅ **Badges coloridas** diferenciando cada fonte (badge verde especial para sites oficiais)  
✅ Interface responsiva e moderna (Tailwind)  
✅ Backend com CORS liberado para o frontend local  

---

## 📡 Fontes de Dados

> 📖 **Documentação completa:** Veja [FONTES.md](./FONTES.md) para detalhes técnicos de cada fonte

### 🏢 Fonte Prioritária (NOVO!)
| Fonte | Tipo | API Key? | Descrição |
|-------|------|----------|-----------|
| **🌟 Site Oficial da Empresa** | RSS/Scraping | ❌ Não | Busca direta no site oficial (Nubank, Totvs, Stone, Magazine Luiza, Mercado Livre, Natura) |

### 🇧🇷 Fontes Brasileiras
| Fonte | Tipo | API Key? | Descrição |
|-------|------|----------|-----------|
| **Google News** | RSS | ❌ Não | Feed de notícias globais (últimos 7 dias) |
| **G1 Globo** | RSS | ❌ Não | Principal portal de notícias do Brasil |
| **InfoMoney** | RSS | ❌ Não | Especializado em economia e mercado financeiro |
| **UOL Economia** | RSS | ❌ Não | Notícias de economia e negócios |

### 🌍 Fontes Internacionais
| Fonte | Tipo | API Key? | Descrição |
|-------|------|----------|-----------|
| **Reuters** | RSS | ❌ Não | Agência de notícias internacional |
| **Yahoo Finance** | RSS | ❌ Não | Notícias financeiras e de empresas |
| **DuckDuckGo** | Scraping | ❌ Não | Buscador com foco em privacidade |
| **LinkedIn** | API (SerpAPI) | ✅ Sim | Postagens corporativas no LinkedIn |
| **Bing News** | API | ✅ Sim | API de notícias da Microsoft |

### 🔑 Configuração de API Keys (Opcional)

> 📖 **Guia completo:** Veja [backend/ENV_SETUP.md](./backend/ENV_SETUP.md) para instruções detalhadas

Crie um arquivo `.env` na pasta `backend/`:

```bash
# Opcional - LinkedIn via SerpAPI
SERP_API_KEY=sua_chave_serpapi_aqui

# Opcional - Bing News API
BING_API_KEY=sua_chave_bing_aqui

# Opcional - OpenAI para classificação com IA
OPENAI_API_KEY=sua_chave_openai_aqui
```

**Nota:** O sistema funciona sem nenhuma API key, buscando nas **7 fontes gratuitas**!

### 🎨 Identificação Visual das Fontes

Cada fonte possui uma **badge colorida** no frontend para fácil identificação:

```
🌟 Verde Esmeralda (destaque) → Site Oficial da Empresa
🔵 Azul                       → Google News
🟣 Roxo                       → LinkedIn  
🟢 Verde                      → G1 Globo
🟡 Amarelo                    → InfoMoney
🔷 Ciano                      → UOL Economia
🔴 Vermelho                   → Reuters
🟪 Púrpura                    → Yahoo Finance
🟠 Laranja                    → DuckDuckGo
🟦 Teal                       → Bing News
```

**Nota:** Notícias do site oficial da empresa aparecem em **negrito** com badge especial!

---

## ⚙️ Como rodar localmente

### 🔹 Backend (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt

# Teste as fontes de dados (opcional)
python test_sources.py

# Inicie o servidor
uvicorn main:app --reload --port 8000
```

Servidor disponível em: `http://localhost:8000`  
Documentação interativa em: `http://localhost:8000/docs`

### 🔹 Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Aplicação disponível em: `http://localhost:5173`

### 🔹 Com Docker Compose

```bash
docker-compose up --build
```

- Frontend: `http://localhost:8080`
- Backend: `http://localhost:8000`

---

## 📖 Documentação Adicional

| Documento | Descrição |
|-----------|-----------|
| 📡 [FONTES.md](./FONTES.md) | Documentação técnica completa de todas as 9 fontes de dados |
| 🔑 [ENV_SETUP.md](./backend/ENV_SETUP.md) | Guia detalhado de configuração de API keys opcionais |
| 📝 [CHANGELOG.md](./CHANGELOG.md) | Histórico de versões e mudanças do projeto |
| 🚀 [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) | Resumo executivo da implementação v2.0 |
| 🧪 [test_sources.py](./backend/test_sources.py) | Script de teste automatizado das fontes |

---

## 🌟 Destaques da Versão 2.1 (Atual)

```
🏢 NOVO: Busca direta no site oficial das empresas
📅 NOVO: Ordenação automática por data (mais recentes primeiro)
🕒 NOVO: Filtro temporal - apenas notícias dos últimos 7 dias
🚀 10 fontes de dados diferentes (2 → 10 fontes = +400%)
🌍 Cobertura global + brasileira completa
🎨 Sistema visual de badges coloridas (10 cores)
📊 8 fontes 100% gratuitas sem limitações
🧪 Suite de testes automatizados com verificação de ordenação
📚 Documentação profissional expandida
```

### 📈 Empresas com Site Oficial Integrado

✅ **Nubank** - Blog e Imprensa  
✅ **Totvs** - Sala de Imprensa  
✅ **Stone** - Investor Relations  
✅ **Magazine Luiza** - Relações com Investidores  
✅ **Mercado Livre** - Sala de Imprensa  
✅ **Natura** - Sala de Imprensa  

*Mais empresas sendo adicionadas continuamente!*

---

## 🤝 Contribuindo

Sugestões de novas fontes ou melhorias são bem-vindas! Abra uma **issue** ou **pull request**.

### Roadmap de Fontes Futuras
- [ ] Estadão (RSS)
- [ ] Folha de S.Paulo (RSS)
- [ ] Bloomberg (API)
- [ ] Valor Econômico (RSS)

---

## 📄 Licença

MIT License - use livremente!

---

**Market News Monitor v2.1** - Smart News Edition 🚀  
*Com busca em sites oficiais, ordenação por data e filtro temporal*
