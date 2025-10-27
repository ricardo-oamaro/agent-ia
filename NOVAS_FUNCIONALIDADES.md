# 🎉 Novas Funcionalidades Implementadas

## 📋 Resumo das Melhorias

As seguintes funcionalidades foram adicionadas ao **Market News Monitor** para melhorar a qualidade e relevância das notícias:

---

## 1️⃣ 🕒 Busca de Notícias Mais Recentes

### O que mudou:
- **Filtro temporal** aplicado em todas as fontes principais
- Priorização de conteúdo dos **últimos 7 dias**
- Parâmetros de "freshness" nas APIs

### Implementações técnicas:

#### Google News
```python
# Antes: sem filtro temporal
url = f"https://news.google.com/rss/search?q={company}"

# Depois: filtro dos últimos 7 dias
query = urllib.parse.quote(f"{company} when:7d")
url = f"https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt"
```

#### Bing News API
```python
params = {
    "q": company,
    "mkt": "pt-BR",
    "count": 10,
    "freshness": "Week"  # Últimos 7 dias
}
```

### Benefícios:
✅ Notícias sempre atualizadas  
✅ Elimina conteúdo obsoleto  
✅ Melhor relevância temporal  
✅ Resposta mais rápida (menos dados processados)  

---

## 2️⃣ 📅 Ordenação por Data (Mais Recentes Primeiro)

### O que mudou:
- **Todas as notícias são ordenadas por data** antes de serem enviadas ao frontend
- Notícias mais recentes aparecem **primeiro**
- Notícias sem data são colocadas no final

### Implementação técnica:

```python
def sort_by_date(news_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Ordena lista de notícias por data (mais recente primeiro)"""
    def parse_date(news_item):
        published_at = news_item.get("published_at")
        
        if not published_at:
            return datetime.min  # Sem data vai para o final
        
        try:
            # Formato principal: "DD/MM/YYYY HH:MM"
            if "/" in published_at and ":" in published_at:
                dt = datetime.strptime(published_at, "%d/%m/%Y %H:%M")
                return dt
            
            # Tenta outros formatos comuns
            for fmt in ["%Y-%m-%d %H:%M:%S", "%d/%m/%Y", "%Y-%m-%d"]:
                try:
                    return datetime.strptime(published_at, fmt)
                except:
                    continue
            
            return datetime.min
        except:
            return datetime.min
    
    # Ordena por data (reverse=True para mais recente primeiro)
    sorted_news = sorted(news_list, key=parse_date, reverse=True)
    return sorted_news
```

### Integração no agregador:

```python
def fetch_real_news(companies: List[str]) -> List[Dict[str, str]]:
    results = []
    
    # ... busca em todas as fontes ...
    
    # 📅 ORDENAÇÃO POR DATA
    results = sort_by_date(results)
    print(f"📅 Notícias ordenadas por data (mais recentes primeiro)\n")
    
    return results
```

### Benefícios:
✅ Usuário vê as **últimas notícias primeiro**  
✅ Experiência de usuário melhorada  
✅ Não precisa rolar para encontrar novidades  
✅ Funciona com múltiplos formatos de data  
✅ Tratamento robusto de erros (notícias sem data não quebram o sistema)  

---

## 3️⃣ 🏢 Busca nos Sites Oficiais das Empresas

### O que mudou:
- **Nova fonte de dados:** Sites oficiais das empresas
- **Prioridade máxima:** Buscado primeiro (fonte mais confiável)
- **Badge especial:** Verde esmeralda em negrito para destacar

### Empresas suportadas:

| Empresa | RSS | Página de Notícias | Sala de Imprensa |
|---------|-----|-------------------|------------------|
| **Nubank** | ✅ | ✅ | ✅ |
| **Totvs** | ❌ | ✅ | ✅ |
| **Stone** | ❌ | ✅ | ✅ |
| **Magazine Luiza** | ❌ | ✅ | ✅ |
| **Mercado Livre** | ❌ | ✅ | ✅ |
| **Natura** | ❌ | ✅ | ✅ |

### Implementação técnica:

```python
def fetch_company_website_news(companies: List[str]) -> List[Dict[str, str]]:
    """Tenta buscar notícias diretamente do site oficial da empresa"""
    results = []
    
    # Mapeamento de empresas conhecidas
    company_urls = {
        "nubank": {
            "rss": "https://nubank.com.br/rss",
            "news_page": "https://blog.nubank.com.br/",
            "press": "https://nubank.com.br/imprensa/"
        },
        "totvs": {
            "news_page": "https://www.totvs.com/sala-de-imprensa/",
            "press": "https://www.totvs.com/sala-de-imprensa/"
        },
        # ... mais empresas ...
    }
    
    for company in companies:
        company_lower = company.lower()
        
        if company_lower not in company_urls:
            print(f"⚠️  Site oficial: Empresa '{company}' não mapeada")
            continue
        
        urls = company_urls[company_lower]
        
        # 1. Tenta RSS primeiro (mais confiável)
        if "rss" in urls:
            try:
                r = httpx.get(urls["rss"], timeout=10, follow_redirects=True)
                soup = BeautifulSoup(r.content, "xml")
                items = soup.find_all("item")
                
                for it in items[:5]:
                    # Extrai dados do RSS...
                    results.append({
                        "company": company,
                        "title": title,
                        "description": description,
                        "url": link,
                        "fonte": f"{company} Oficial",
                        "fonte_type": "company_website",
                        "published_at": published_at,
                    })
            except Exception as e:
                print(f"⚠️  Erro ao buscar RSS de {company}: {e}")
        
        # 2. Se não tiver RSS, faz scraping da página
        news_url = urls.get("press") or urls.get("news_page")
        if news_url:
            try:
                headers = {"User-Agent": "Mozilla/5.0 ..."}
                r = httpx.get(news_url, headers=headers, timeout=10)
                soup = BeautifulSoup(r.content, "html.parser")
                
                # Busca elementos comuns de notícias
                news_elements = (
                    soup.find_all("article", limit=5) or
                    soup.find_all("div", class_=lambda x: x and "news" in x.lower(), limit=5)
                )
                
                for elem in news_elements:
                    # Extrai título, link e descrição...
                    results.append({...})
                    
            except Exception as e:
                print(f"⚠️  Erro ao buscar site de {company}: {e}")
    
    return results
```

### Estratégia de busca:

1. **RSS Feed** (se disponível) - Mais confiável e estruturado
2. **Web Scraping** (fallback) - Para sites sem RSS
3. **Elementos genéricos** - article, div com "news", h2

### Badge especial no frontend:

```javascript
case "company_website":
    return "bg-emerald-100 text-emerald-700 font-bold"; // Verde esmeralda em negrito
```

### Benefícios:
✅ **Fonte oficial** - informação direto da empresa  
✅ **Confiabilidade máxima** - sem intermediários  
✅ **Comunicados oficiais** - releases, anúncios, eventos  
✅ **Prioridade visual** - badge verde destaca conteúdo oficial  
✅ **Fácil expansão** - adicionar novas empresas no mapeamento  
✅ **Fallback inteligente** - tenta RSS primeiro, depois scraping  

---

## 🎨 Identificação Visual

### Novas badges:

| Fonte | Cor | Tipo |
|-------|-----|------|
| **Site Oficial** | 🟢 Verde Esmeralda (negrito) | `company_website` |
| Google News | 🔵 Azul | `google` |
| LinkedIn | 🟣 Roxo | `linkedin` |
| G1 Globo | 🟢 Verde | `g1` |
| InfoMoney | 🟡 Amarelo | `infomoney` |
| UOL | 🔷 Ciano | `uol` |
| Reuters | 🔴 Vermelho | `reuters` |
| Yahoo Finance | 🟪 Púrpura | `yahoo` |
| DuckDuckGo | 🟠 Laranja | `duckduckgo` |
| Bing News | 🟦 Teal | `bing` |

---

## 📊 Estatísticas

### Antes vs Depois

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| **Fontes de dados** | 9 | 10 | +11% |
| **Relevância temporal** | Sem filtro | Últimos 7 dias | ✅ |
| **Ordenação** | Aleatória | Por data | ✅ |
| **Fontes oficiais** | 0 | 6 empresas | ✅ |
| **Experiência do usuário** | Boa | Excelente | 🚀 |

---

## 🧪 Como Testar

### 1. Teste rápido das fontes:

```bash
cd backend
python test_sources.py
```

**Saída esperada:**
```
🧪 Testando: Site Oficial da Empresa
✅ Site Oficial da Empresa: X notícias encontradas

📰 Exemplo de notícia:
   Empresa: Nubank
   Título: Nubank anuncia...
   Fonte: Nubank Oficial (company_website)
   URL: https://nubank.com.br/...
```

### 2. Teste no frontend:

```bash
# Terminal 1 - Backend
cd backend
uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**No navegador (http://localhost:5173):**

1. Digite: `Nubank, Totvs, Stone`
2. Clique em **"Atualizar"**
3. Observe:
   - ✅ Notícias ordenadas por data (mais recentes no topo)
   - ✅ Badges **verdes em negrito** para sites oficiais
   - ✅ Datas formatadas "há X horas" ou "há X dias"
   - ✅ Mix de fontes (oficial + portais + internacional)

### 3. Validação da ordenação:

Verifique se as datas estão em ordem decrescente:
- Primeira notícia: "há 2 horas"
- Segunda notícia: "há 5 horas"
- Terceira notícia: "há 1 dia"
- ...

---

## 🔧 Manutenção

### Adicionar nova empresa no sistema:

Edite `/backend/data_source.py` e adicione ao dicionário `company_urls`:

```python
company_urls = {
    # ... empresas existentes ...
    
    "nova empresa": {
        "rss": "https://novaempresa.com/rss",  # Se tiver RSS
        "news_page": "https://novaempresa.com/noticias/",
        "press": "https://novaempresa.com/imprensa/"
    },
}
```

### Empresas prioritárias para adicionar:

- [ ] **B3** (Bolsa de Valores)
- [ ] **Itaú**
- [ ] **Bradesco**
- [ ] **Banco do Brasil**
- [ ] **Petrobras**
- [ ] **Vale**
- [ ] **Ambev**
- [ ] **Weg**

---

## 🐛 Troubleshooting

### Problema: Notícias não estão ordenadas

**Causa:** Formato de data incompatível  
**Solução:** Adicionar formato ao parser em `sort_by_date()`

### Problema: Site oficial não retorna notícias

**Causa 1:** Empresa não mapeada  
**Solução:** Adicionar ao `company_urls`

**Causa 2:** Site mudou estrutura HTML  
**Solução:** Ajustar seletores CSS no scraping

**Causa 3:** Site bloqueia bot  
**Solução:** Melhorar User-Agent ou adicionar delay

### Problema: Badge não aparece verde

**Causa:** `fonte_type` diferente de `company_website`  
**Solução:** Verificar backend retorna tipo correto

---

## 📈 Próximas Melhorias Sugeridas

### Curto Prazo
- [ ] **Cache de sites oficiais** (15 minutos) para performance
- [ ] **Mais empresas** no mapeamento (B3, bancos, etc)
- [ ] **Detecção automática** de RSS feeds
- [ ] **Fallback para Wayback Machine** se site estiver offline

### Médio Prazo
- [ ] **Scraping inteligente** com Machine Learning
- [ ] **Monitoramento de uptime** dos sites oficiais
- [ ] **Notificações** quando empresa publica novo conteúdo
- [ ] **Análise de sentimento** do conteúdo oficial

### Longo Prazo
- [ ] **API das empresas** quando disponível
- [ ] **Integração com IR** (relações com investidores)
- [ ] **Transcrições de earnings calls**
- [ ] **Análise de impacto** nas ações

---

## ✅ Checklist de Validação

### Funcionalidade 1: Notícias Recentes
- [x] Google News filtra últimos 7 dias
- [x] Bing News usa parâmetro `freshness: "Week"`
- [x] Fontes RSS principais atualizadas
- [x] Logs mostram data das notícias encontradas

### Funcionalidade 2: Ordenação
- [x] Função `sort_by_date()` implementada
- [x] Integrada no `fetch_real_news()`
- [x] Suporta múltiplos formatos de data
- [x] Notícias sem data vão para o final
- [x] Frontend mostra em ordem correta

### Funcionalidade 3: Sites Oficiais
- [x] Função `fetch_company_website_news()` implementada
- [x] 6 empresas mapeadas inicialmente
- [x] Suporta RSS e scraping
- [x] Badge verde especial no frontend
- [x] Prioridade na busca (executado primeiro)
- [x] Tratamento de erros robusto

---

## 🎉 Conclusão

As três funcionalidades foram **implementadas com sucesso** e estão prontas para produção:

1. ✅ **Notícias mais recentes** - Filtro temporal de 7 dias
2. ✅ **Ordenação por data** - Mais recentes primeiro
3. ✅ **Sites oficiais** - 10ª fonte de dados

**Resultado:** Sistema mais relevante, organizado e confiável! 🚀

---

**Última atualização:** Outubro 2025  
**Versão:** 2.1.0 - Recent News Edition

