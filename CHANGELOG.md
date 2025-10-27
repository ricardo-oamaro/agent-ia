# 📝 Changelog - Market News Monitor

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

---

## [2.0.0] - 2025-10-24 🚀 Multi-Source Edition

### ✨ Novas Funcionalidades

#### 🌎 Expansão Massiva de Fontes de Dados
- **8 novas fontes** adicionadas ao sistema (anteriormente apenas 2)
- Total de **9 fontes diferentes** de notícias
- Cobertura ampliada: Brasil + Internacional

#### 🇧🇷 Fontes Brasileiras Adicionadas
- ✅ **G1 Globo** - Principal portal de notícias do Brasil (RSS)
- ✅ **InfoMoney** - Especializado em economia e mercado financeiro (RSS)
- ✅ **UOL Economia** - Notícias de economia e negócios (RSS)

#### 🌍 Fontes Internacionais Adicionadas
- ✅ **Reuters** - Agência de notícias global (RSS multi-feed)
- ✅ **Yahoo Finance** - Notícias financeiras e de mercado (RSS)
- ✅ **DuckDuckGo** - Buscador com foco em privacidade (Web Scraping)
- ✅ **Bing News** - API de notícias da Microsoft (API opcional)

#### 🎨 Melhorias Visuais
- Sistema de **badges coloridas** por fonte no frontend
- 9 cores diferentes para identificação rápida:
  - 🔵 Azul (Google), 🟣 Roxo (LinkedIn), 🟢 Verde (G1)
  - 🟡 Amarelo (InfoMoney), 🔷 Ciano (UOL), 🔴 Vermelho (Reuters)
  - 🟪 Púrpura (Yahoo), 🟠 Laranja (DuckDuckGo), 🟦 Teal (Bing)
- Componente `NewsCard.jsx` atualizado com suporte a todas as fontes

### 🔧 Melhorias Técnicas

#### Backend (`data_source.py`)
- Refatoração completa do sistema de busca
- Implementação de 7 novas funções de scraping:
  - `fetch_bing_news()` - Integração com Bing News API
  - `fetch_g1_news()` - Parser RSS do G1
  - `fetch_infomoney_news()` - Parser RSS do InfoMoney
  - `fetch_uol_news()` - Parser RSS do UOL
  - `fetch_reuters_news()` - Multi-feed RSS da Reuters
  - `fetch_yahoo_finance_news()` - RSS do Yahoo Finance
  - `fetch_duckduckgo_news()` - Web scraping do DuckDuckGo
- Agregador `fetch_real_news()` totalmente reescrito
- Sistema de logging aprimorado com emojis e contadores
- Tratamento robusto de erros individuais por fonte

#### Tratamento de Dados
- Parser de datas com múltiplos formatos suportados
- Filtragem inteligente por relevância (título + descrição)
- Normalização de URLs e metadados
- Suporte a encoding UTF-8 para fontes brasileiras

#### Configuração
- Nova variável `BING_API_KEY` para Bing News API
- Importação de `urllib.parse` para encoding de URLs
- Importação de `re` para expressões regulares

### 📚 Documentação

#### Novos Arquivos
- ✅ **FONTES.md** - Documentação técnica completa de todas as fontes
  - Detalhes de cada fonte (URL, tipo, limites)
  - Comparativo visual entre fontes
  - Instruções de obtenção de API keys
  - Roadmap de futuras fontes
- ✅ **test_sources.py** - Script de teste automatizado
  - Testa todas as 9 fontes individualmente
  - Exibe exemplos de notícias encontradas
  - Relatório de status de cada fonte
  - Diagnóstico de problemas
- ✅ **CHANGELOG.md** - Este arquivo

#### Atualizações no README
- Seção expandida "Fontes de Dados"
- Tabelas com todas as fontes (brasileiras e internacionais)
- Guia de configuração de API keys opcionais
- Seção "Identificação Visual das Fontes"
- Link para documentação técnica (FONTES.md)
- Instruções de teste (`python test_sources.py`)

### 🐛 Correções de Bugs
- **Fix:** LinkedIn agora processa múltiplas empresas corretamente
- **Fix:** Tratamento de charset em feeds RSS brasileiros
- **Fix:** Parsing de datas com múltiplos formatos timezone

### ⚡ Performance
- Sistema agora **resiliente a falhas**: uma fonte offline não impacta as outras
- Timeout de 10s por requisição para evitar travamentos
- Logging detalhado para debugging

### 🔒 Segurança
- User-Agent customizado para DuckDuckGo (evita bloqueio)
- Validação de API keys antes de fazer requisições
- Tratamento seguro de exceções em todas as fontes

---

## [1.0.0] - 2025-10-XX 📰 Initial Release

### ✨ Funcionalidades Iniciais
- Sistema de busca de notícias por empresa
- 2 fontes de dados:
  - Google News RSS
  - LinkedIn via SerpAPI
- Frontend React + Vite + Tailwind
- Backend FastAPI
- Sistema de filtros por evento
- Cards clicáveis com links para fonte original

### 🏗️ Arquitetura Base
- Containerização com Docker
- API REST com FastAPI
- Interface moderna com TailwindCSS
- Componentes React modulares

---

## 📊 Estatísticas de Crescimento

| Versão | Fontes | Arquivos Python | Linhas de Código | Documentação |
|--------|--------|-----------------|------------------|--------------|
| 1.0.0  | 2      | 4               | ~200             | README.md    |
| 2.0.0  | 9      | 5               | ~580             | README.md + FONTES.md + CHANGELOG.md + test_sources.py |

**Crescimento:** 
- 📈 **+350%** em fontes de dados
- 📈 **+190%** em linhas de código
- 📈 **+400%** em documentação

---

## 🎯 Próximos Passos (Roadmap)

### Versão 2.1.0 (Próxima)
- [ ] Requisições paralelas com `asyncio`
- [ ] Cache Redis (TTL 15 minutos)
- [ ] Deduplicação inteligente de notícias
- [ ] Adicionar Estadão e Folha de S.Paulo

### Versão 2.2.0
- [ ] Análise de sentimento das notícias
- [ ] Sistema de alertas em tempo real
- [ ] Integração com Twitter/X
- [ ] Dashboard de analytics

### Versão 3.0.0
- [ ] Machine Learning para relevância
- [ ] Sistema multi-agente (baseado em CPS)
- [ ] API GraphQL
- [ ] Aplicativo mobile

---

## 🤝 Contribuindo

Sugestões de novas fontes? Issues e PRs são bem-vindos!

Prioridades para novas fontes:
1. Bloomberg (API)
2. Financial Times (Scraping)
3. Valor Econômico (RSS)
4. Exame (RSS)

---

**Mantido por:** [Seu Nome]  
**Licença:** MIT  
**Última atualização:** 24 de Outubro de 2025

