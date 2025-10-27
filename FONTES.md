# 📡 Documentação das Fontes de Notícias

Este documento detalha todas as fontes de dados implementadas no Market News Monitor.

---

## 🇧🇷 Fontes Brasileiras

### 1. Google News Brasil
- **Tipo:** RSS Feed
- **URL:** `https://news.google.com/rss/search?q={empresa}&hl=pt-BR&gl=BR&ceid=BR:pt`
- **API Key:** ❌ Não necessária
- **Taxa de atualização:** Tempo real
- **Limite por busca:** ~10 artigos
- **Vantagens:**
  - Agregador de múltiplas fontes
  - Sempre atualizado
  - Sem limites de requisição
- **Formato de resposta:** XML/RSS com metadados completos

### 2. G1 Globo
- **Tipo:** RSS Feed
- **URL:** `https://g1.globo.com/dynamo/economia/rss2.xml`
- **API Key:** ❌ Não necessária
- **Taxa de atualização:** A cada hora
- **Limite por busca:** ~5 artigos filtrados
- **Vantagens:**
  - Principal portal de notícias do Brasil
  - Conteúdo de qualidade jornalística
  - Cobertura nacional abrangente
- **Filtragem:** Busca por menção da empresa no título

### 3. InfoMoney
- **Tipo:** RSS Feed
- **URL:** `https://www.infomoney.com.br/feed/`
- **API Key:** ❌ Não necessária
- **Taxa de atualização:** Frequente (várias vezes ao dia)
- **Limite por busca:** ~10 artigos filtrados
- **Vantagens:**
  - Especializado em mercado financeiro
  - Análises de empresas e economia
  - Foco em investimentos
- **Filtragem:** Busca por menção da empresa no título ou descrição

### 4. UOL Economia
- **Tipo:** RSS Feed
- **URL:** `https://rss.uol.com.br/feed/economia.xml`
- **API Key:** ❌ Não necessária
- **Taxa de atualização:** A cada hora
- **Limite por busca:** ~10 artigos filtrados
- **Vantagens:**
  - Grande portal de notícias brasileiro
  - Seção dedicada a economia
  - Ampla cobertura empresarial
- **Filtragem:** Busca por menção da empresa no conteúdo

---

## 🌍 Fontes Internacionais

### 5. Reuters
- **Tipo:** RSS Feed
- **URLs:**
  - `https://www.reuters.com/arc/outboundfeeds/v3/rss/?outputType=xml&size=10`
  - `https://www.reuters.com/business/rss/`
- **API Key:** ❌ Não necessária
- **Taxa de atualização:** Tempo real
- **Limite por busca:** ~10 artigos por feed
- **Vantagens:**
  - Agência de notícias global renomada
  - Cobertura de empresas multinacionais
  - Conteúdo em inglês e português
- **Filtragem:** Busca em múltiplos feeds

### 6. Yahoo Finance
- **Tipo:** RSS Feed
- **URL:** `https://finance.yahoo.com/rss/headline?s={empresa}`
- **API Key:** ❌ Não necessária
- **Taxa de atualização:** Frequente
- **Limite por busca:** ~5 artigos
- **Vantagens:**
  - Especializado em finanças
  - Dados de mercado integrados
  - Cobertura de empresas listadas
- **Formato:** XML/RSS padrão

### 7. DuckDuckGo
- **Tipo:** Web Scraping
- **URL:** `https://html.duckduckgo.com/html/?q={empresa}+news`
- **API Key:** ❌ Não necessária
- **Taxa de atualização:** Tempo real
- **Limite por busca:** ~5 resultados
- **Vantagens:**
  - Sem rastreamento
  - Resultados diversificados
  - Sem bloqueio por rate limiting
- **Observações:** Requer User-Agent customizado

---

## 🔑 Fontes com API (Opcionais)

### 8. LinkedIn (via SerpAPI)
- **Tipo:** API (Google Search para LinkedIn)
- **URL:** `https://serpapi.com/search.json`
- **API Key:** ✅ **SERP_API_KEY** necessária
- **Taxa de atualização:** Sob demanda
- **Limite por busca:** 5 resultados
- **Custo:**
  - Plano gratuito: 100 buscas/mês
  - Plano pago: a partir de $50/mês
- **Vantagens:**
  - Postagens oficiais das empresas
  - Conteúdo corporativo direto
  - Anúncios e atualizações institucionais
- **Como obter:**
  1. Acesse https://serpapi.com/
  2. Crie uma conta gratuita
  3. Copie sua API Key
  4. Adicione no `.env`: `SERP_API_KEY=sua_chave`

### 9. Bing News API
- **Tipo:** REST API (Microsoft Azure)
- **URL:** `https://api.bing.microsoft.com/v7.0/news/search`
- **API Key:** ✅ **BING_API_KEY** necessária
- **Taxa de atualização:** Tempo real
- **Limite por busca:** 10 artigos
- **Custo:**
  - Tier gratuito: 1000 transações/mês
  - S1: $3 por 1000 transações
- **Vantagens:**
  - Cobertura global do Bing
  - Metadados ricos (fonte, data, categoria)
  - Filtragem avançada (idioma, região, data)
- **Como obter:**
  1. Acesse https://portal.azure.com/
  2. Crie recurso "Bing Search v7"
  3. Copie a chave de assinatura
  4. Adicione no `.env`: `BING_API_KEY=sua_chave`

---

## 📊 Comparativo de Fontes

| Fonte | Gratuita | Tempo Real | Brasil | Global | Qualidade |
|-------|----------|------------|--------|--------|-----------|
| Google News | ✅ | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| G1 Globo | ✅ | ⚠️ Hora | ✅ | ❌ | ⭐⭐⭐⭐⭐ |
| InfoMoney | ✅ | ✅ | ✅ | ❌ | ⭐⭐⭐⭐ |
| UOL | ✅ | ⚠️ Hora | ✅ | ❌ | ⭐⭐⭐⭐ |
| Reuters | ✅ | ✅ | ⚠️ | ✅ | ⭐⭐⭐⭐⭐ |
| Yahoo Finance | ✅ | ✅ | ⚠️ | ✅ | ⭐⭐⭐⭐ |
| DuckDuckGo | ✅ | ✅ | ✅ | ✅ | ⭐⭐⭐ |
| LinkedIn | ❌ | ✅ | ✅ | ✅ | ⭐⭐⭐⭐ |
| Bing News | ❌ | ✅ | ✅ | ✅ | ⭐⭐⭐⭐ |

---

## 🔧 Implementação Técnica

### Estrutura das Respostas

Todas as funções retornam uma lista de dicionários com a seguinte estrutura:

```python
{
    "company": str,          # Nome da empresa buscada
    "title": str,            # Título da notícia
    "description": str,      # Descrição/resumo
    "url": str,              # URL da notícia original
    "fonte": str,            # Nome legível da fonte
    "fonte_type": str,       # Identificador da fonte (google, g1, etc)
    "published_at": str      # Data no formato DD/MM/YYYY HH:MM
}
```

### Tratamento de Erros

Todas as funções implementam:
- **Try/Catch individual:** Erro em uma fonte não impacta as outras
- **Timeout de 10s:** Previne travamento em fontes lentas
- **Logging detalhado:** Console mostra sucesso/falha de cada fonte
- **Graceful degradation:** Sistema funciona mesmo com fontes offline

### Performance

- **Requisições em série:** Atualmente sequencial por simplicidade
- **Cache:** Não implementado (potencial melhoria futura)
- **Rate limiting:** Respeitado naturalmente pelo fluxo sequencial

---

## 🚀 Próximas Melhorias

### Curto Prazo
- [ ] Implementar requisições paralelas (asyncio)
- [ ] Adicionar cache Redis (TTL de 15 min)
- [ ] Incluir Estadão (RSS)
- [ ] Incluir Folha de S.Paulo (RSS)

### Médio Prazo
- [ ] Implementar Bloomberg (API)
- [ ] Adicionar Financial Times (scraping)
- [ ] Sistema de priorização de fontes
- [ ] Deduplicação inteligente de notícias

### Longo Prazo
- [ ] Machine Learning para relevância
- [ ] Análise de sentimento das notícias
- [ ] Alertas em tempo real (WebSocket)
- [ ] Integração com redes sociais (Twitter/X)

---

## 📞 Suporte

Para reportar problemas com fontes específicas:
1. Execute `python test_sources.py`
2. Identifique a fonte com erro
3. Verifique conectividade e API keys
4. Consulte a documentação oficial da fonte

---

**Última atualização:** Outubro 2025  
**Versão:** 2.0 - Multi-Source Edition

