import os
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from dotenv import load_dotenv
from datetime import datetime
import re
import urllib.parse

# 🔹 Carrega variáveis de ambiente (.env)
load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")
BING_API_KEY = os.getenv("BING_API_KEY")  # Opcional: Bing News API

# ==============================================================
# 🧩 Utilitários
# ==============================================================

def _soup_xml(xml_bytes):
    """Converte o RSS/XML para BeautifulSoup"""
    try:
        return BeautifulSoup(xml_bytes, "xml")
    except Exception:
        return BeautifulSoup(xml_bytes, "html.parser")

def _first_publisher_link(description_html: str) -> str:
    """Extrai o link real da notícia dentro do HTML do RSS"""
    try:
        soup = BeautifulSoup(description_html or "", "html.parser")
        a = soup.find("a", href=True)
        return a["href"].strip() if a else ""
    except Exception:
        return ""

# ==============================================================
# 🌎 GOOGLE NEWS RSS
# ==============================================================

def fetch_google_news(companies: List[str]) -> List[Dict[str, str]]:
    """Busca notícias via Google News RSS (últimos 7 dias)"""
    results: List[Dict[str, str]] = []

    for company in companies:
        # Adiciona filtro temporal: when:7d (últimos 7 dias)
        query = urllib.parse.quote(f"{company} when:7d")
        url = f"https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt"
        print(f"🔍 Buscando notícias para: {company} → {url}")

        try:
            r = httpx.get(url, timeout=10, follow_redirects=True)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "xml")
            items = soup.find_all("item")

            for it in items[:10]:
                title = (it.title.text or "").strip() if it.title else ""
                link_google = (it.link.text or "").strip() if it.link else ""
                raw_description = (it.description.text or "").strip() if it.description else ""

                # 🔹 Limpa HTML residual da descrição
                try:
                    desc_soup = BeautifulSoup(raw_description, "html.parser")
                    description = desc_soup.get_text(" ", strip=True)
                except Exception:
                    description = raw_description

                # 🔹 Extrai link real da matéria (link do publisher)
                a_tag = BeautifulSoup(raw_description, "html.parser").find("a", href=True)
                article_url = a_tag["href"].strip() if a_tag else link_google
                if not title or not article_url:
                    continue

                # 🔹 Extrai nome da fonte (publisher)
                source_name = ""
                try:
                    font_tag = BeautifulSoup(raw_description, "html.parser").find("font")
                    if font_tag:
                        source_name = font_tag.get_text(strip=True)
                except Exception:
                    pass

                # 🔹 Extrai data (vários formatos possíveis)
                published_at = None
                try:
                    pub_date_tag = (
                        it.find("pubDate") or it.find("dc:date") or it.find("updated")
                    )
                    if pub_date_tag and pub_date_tag.text:
                        date_text = pub_date_tag.text.strip()
                        for fmt in (
                            "%a, %d %b %Y %H:%M:%S %Z",  # Wed, 16 Oct 2025 13:14:00 GMT
                            "%Y-%m-%dT%H:%M:%S%z",     # 2025-10-16T13:14:00+0000
                            "%Y-%m-%dT%H:%M:%SZ",      # 2025-10-16T13:14:00Z
                        ):
                            try:
                                dt = datetime.strptime(date_text, fmt)
                                published_at = dt.strftime("%d/%m/%Y %H:%M")
                                break
                            except Exception:
                                continue
                        if not published_at:
                            published_at = date_text
                except Exception as e:
                    print(f"⚠️ Erro ao ler data de {company}: {e}")

                # 🔹 Loga o item encontrado
                print(f"🕒 {company} → {title[:50]}... → {published_at or 'sem data'}")

                # 🔹 Monta o dicionário compatível com o modelo
                results.append({
                    "company": company,
                    "title": title,
                    "description": description,
                    "url": article_url,
                    "fonte": source_name or "Google News",
                    "fonte_type": "google",
                    "published_at": published_at,
                })

        except Exception as e:
            print(f"⚠️ Erro ao buscar Google News para {company}: {e}")

    print(f"✅ Google News: {len(results)} resultados no total.")
    return results

# ==============================================================
# 🔗 LINKEDIN VIA SERPAPI
# ==============================================================

def fetch_linkedin_posts(company: str) -> List[Dict[str, str]]:
    """Busca postagens do LinkedIn via SerpApi (Google search)"""
    results = []
    if not SERP_API_KEY:
        print("⚠️ SERP_API_KEY não configurada no .env")
        return results

    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": f"site:linkedin.com/company {company}",
        "api_key": SERP_API_KEY,
        "hl": "pt-BR",
        "num": 5,
    }

    try:
        r = httpx.get(url, params=params, timeout=15)
        r.raise_for_status()

        if "application/json" not in r.headers.get("content-type", ""):
            print(f"⚠️ Resposta não JSON da SerpApi: {r.text[:200]}")
            return results

        data = r.json()
        
        # 🔹 Extrai data do search_metadata (created_at)
        search_created_at = None
        try:
            search_metadata = data.get("search_metadata", {})
            created_at_text = search_metadata.get("created_at", "")
            if created_at_text:
                # Formato: "2025-10-21 18:58:25 UTC"
                dt = datetime.strptime(created_at_text, "%Y-%m-%d %H:%M:%S UTC")
                search_created_at = dt.strftime("%d/%m/%Y %H:%M")
                print(f"📅 LinkedIn {company}: Data da busca - {search_created_at}")
        except Exception as e:
            print(f"⚠️ Erro ao processar created_at do LinkedIn para {company}: {e}")
        
        for item in data.get("organic_results", []):
            results.append({
                "company": company,
                "title": item.get("title", ""),
                "description": item.get("snippet", ""),
                "url": item.get("link", ""),
                "fonte": "LinkedIn",
                "fonte_type": "linkedin",
                "published_at": search_created_at,  # Usa a data da busca como referência
            })
        print(f"🔗 LinkedIn: {len(results)} resultados para {company}")
    except Exception as e:
        print(f"⚠️ Erro ao buscar LinkedIn para {company}: {e}")

    return results

# ==============================================================
# 🌍 BING NEWS SEARCH
# ==============================================================

def fetch_bing_news(companies: List[str]) -> List[Dict[str, str]]:
    """Busca notícias via Bing News Search API"""
    results = []
    
    if not BING_API_KEY:
        print("⚠️ BING_API_KEY não configurada - pulando Bing News")
        return results
    
    for company in companies:
        url = "https://api.bing.microsoft.com/v7.0/news/search"
        headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
        params = {
            "q": company,
            "mkt": "pt-BR",
            "count": 10,
            "freshness": "Week"
        }
        
        try:
            r = httpx.get(url, headers=headers, params=params, timeout=10)
            r.raise_for_status()
            data = r.json()
            
            for article in data.get("value", []):
                published_at = None
                if article.get("datePublished"):
                    try:
                        dt = datetime.fromisoformat(article["datePublished"].replace("Z", "+00:00"))
                        published_at = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        published_at = article.get("datePublished")
                
                results.append({
                    "company": company,
                    "title": article.get("name", ""),
                    "description": article.get("description", ""),
                    "url": article.get("url", ""),
                    "fonte": article.get("provider", [{}])[0].get("name", "Bing News"),
                    "fonte_type": "bing",
                    "published_at": published_at,
                })
            
            print(f"🔵 Bing News: {len(results)} resultados para {company}")
        except Exception as e:
            print(f"⚠️ Erro ao buscar Bing News para {company}: {e}")
    
    return results

# ==============================================================
# 📰 G1 GLOBO (RSS)
# ==============================================================

def fetch_g1_news(companies: List[str]) -> List[Dict[str, str]]:
    """Busca notícias no G1 via RSS"""
    results = []
    
    for company in companies:
        # G1 tem RSS de busca
        query = urllib.parse.quote(company)
        url = f"https://g1.globo.com/dynamo/economia/rss2.xml"
        
        try:
            r = httpx.get(url, timeout=10, follow_redirects=True)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "xml")
            items = soup.find_all("item")
            
            for it in items[:5]:
                title = (it.title.text or "").strip() if it.title else ""
                # Filtra apenas notícias que mencionam a empresa
                if company.lower() not in title.lower():
                    continue
                
                description = (it.description.text or "").strip() if it.description else ""
                link = (it.link.text or "").strip() if it.link else ""
                
                published_at = None
                if it.pubDate:
                    try:
                        date_text = it.pubDate.text.strip()
                        dt = datetime.strptime(date_text, "%a, %d %b %Y %H:%M:%S %z")
                        published_at = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        published_at = it.pubDate.text
                
                results.append({
                    "company": company,
                    "title": title,
                    "description": description,
                    "url": link,
                    "fonte": "G1 Globo",
                    "fonte_type": "g1",
                    "published_at": published_at,
                })
            
            print(f"🟢 G1: {len([r for r in results if r['company']==company])} resultados para {company}")
        except Exception as e:
            print(f"⚠️ Erro ao buscar G1 para {company}: {e}")
    
    return results

# ==============================================================
# 📊 INFOMONEY (RSS)
# ==============================================================

def fetch_infomoney_news(companies: List[str]) -> List[Dict[str, str]]:
    """Busca notícias no InfoMoney via RSS"""
    results = []
    
    for company in companies:
        url = "https://www.infomoney.com.br/feed/"
        
        try:
            r = httpx.get(url, timeout=10, follow_redirects=True)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "xml")
            items = soup.find_all("item")
            
            for it in items[:10]:
                title = (it.title.text or "").strip() if it.title else ""
                description = (it.description.text or "").strip() if it.description else ""
                
                # Filtra notícias relevantes à empresa
                full_text = f"{title} {description}".lower()
                if company.lower() not in full_text:
                    continue
                
                link = (it.link.text or "").strip() if it.link else ""
                
                published_at = None
                if it.pubDate:
                    try:
                        date_text = it.pubDate.text.strip()
                        dt = datetime.strptime(date_text, "%a, %d %b %Y %H:%M:%S %z")
                        published_at = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        published_at = it.pubDate.text
                
                results.append({
                    "company": company,
                    "title": title,
                    "description": description,
                    "url": link,
                    "fonte": "InfoMoney",
                    "fonte_type": "infomoney",
                    "published_at": published_at,
                })
            
            print(f"💰 InfoMoney: {len([r for r in results if r['company']==company])} resultados para {company}")
        except Exception as e:
            print(f"⚠️ Erro ao buscar InfoMoney para {company}: {e}")
    
    return results

# ==============================================================
# 🌎 REUTERS (RSS)
# ==============================================================

def fetch_reuters_news(companies: List[str]) -> List[Dict[str, str]]:
    """Busca notícias na Reuters via RSS"""
    results = []
    
    # Reuters tem vários feeds RSS
    feeds = [
        "https://www.reuters.com/arc/outboundfeeds/v3/rss/?outputType=xml&size=10",
        "https://www.reuters.com/business/rss/",
    ]
    
    for company in companies:
        for feed_url in feeds:
            try:
                r = httpx.get(feed_url, timeout=10, follow_redirects=True)
                r.raise_for_status()
                soup = BeautifulSoup(r.content, "xml")
                items = soup.find_all("item")
                
                for it in items[:10]:
                    title = (it.title.text or "").strip() if it.title else ""
                    description = (it.description.text or "").strip() if it.description else ""
                    
                    # Filtra notícias relevantes
                    full_text = f"{title} {description}".lower()
                    if company.lower() not in full_text:
                        continue
                    
                    link = (it.link.text or "").strip() if it.link else ""
                    
                    published_at = None
                    pub_date_tag = it.find("pubDate") or it.find("dc:date")
                    if pub_date_tag:
                        try:
                            date_text = pub_date_tag.text.strip()
                            dt = datetime.strptime(date_text, "%a, %d %b %Y %H:%M:%S %z")
                            published_at = dt.strftime("%d/%m/%Y %H:%M")
                        except:
                            published_at = pub_date_tag.text
                    
                    results.append({
                        "company": company,
                        "title": title,
                        "description": description,
                        "url": link,
                        "fonte": "Reuters",
                        "fonte_type": "reuters",
                        "published_at": published_at,
                    })
                
            except Exception as e:
                print(f"⚠️ Erro ao buscar Reuters ({feed_url}) para {company}: {e}")
        
        print(f"📰 Reuters: {len([r for r in results if r['company']==company])} resultados para {company}")
    
    return results

# ==============================================================
# 💼 YAHOO FINANCE (RSS)
# ==============================================================

def fetch_yahoo_finance_news(companies: List[str]) -> List[Dict[str, str]]:
    """Busca notícias no Yahoo Finance"""
    results = []
    
    for company in companies:
        query = urllib.parse.quote(company)
        url = f"https://finance.yahoo.com/rss/headline?s={query}"
        
        try:
            r = httpx.get(url, timeout=10, follow_redirects=True)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "xml")
            items = soup.find_all("item")
            
            for it in items[:5]:
                title = (it.title.text or "").strip() if it.title else ""
                description = (it.description.text or "").strip() if it.description else ""
                link = (it.link.text or "").strip() if it.link else ""
                
                published_at = None
                if it.pubDate:
                    try:
                        date_text = it.pubDate.text.strip()
                        dt = datetime.strptime(date_text, "%a, %d %b %Y %H:%M:%S %z")
                        published_at = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        published_at = it.pubDate.text
                
                results.append({
                    "company": company,
                    "title": title,
                    "description": description,
                    "url": link,
                    "fonte": "Yahoo Finance",
                    "fonte_type": "yahoo",
                    "published_at": published_at,
                })
            
            print(f"💹 Yahoo Finance: {len([r for r in results if r['company']==company])} resultados para {company}")
        except Exception as e:
            print(f"⚠️ Erro ao buscar Yahoo Finance para {company}: {e}")
    
    return results

# ==============================================================
# 🦆 DUCKDUCKGO NEWS
# ==============================================================

def fetch_duckduckgo_news(companies: List[str]) -> List[Dict[str, str]]:
    """Busca notícias via DuckDuckGo (HTML scraping)"""
    results = []
    
    for company in companies:
        query = urllib.parse.quote(f"{company} news")
        url = f"https://html.duckduckgo.com/html/?q={query}"
        
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            r = httpx.get(url, headers=headers, timeout=10, follow_redirects=True)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "html.parser")
            
            # DuckDuckGo usa divs com classe específica para resultados
            result_divs = soup.find_all("div", class_="result__body")
            
            for div in result_divs[:5]:
                title_tag = div.find("a", class_="result__a")
                snippet_tag = div.find("a", class_="result__snippet")
                
                if not title_tag:
                    continue
                
                title = title_tag.get_text(strip=True)
                link = title_tag.get("href", "")
                description = snippet_tag.get_text(strip=True) if snippet_tag else ""
                
                results.append({
                    "company": company,
                    "title": title,
                    "description": description,
                    "url": link,
                    "fonte": "DuckDuckGo",
                    "fonte_type": "duckduckgo",
                    "published_at": None,
                })
            
            print(f"🦆 DuckDuckGo: {len([r for r in results if r['company']==company])} resultados para {company}")
        except Exception as e:
            print(f"⚠️ Erro ao buscar DuckDuckGo para {company}: {e}")
    
    return results

# ==============================================================
# 📄 UOL ECONOMIA (RSS)
# ==============================================================

def fetch_uol_news(companies: List[str]) -> List[Dict[str, str]]:
    """Busca notícias no UOL Economia via RSS"""
    results = []
    
    for company in companies:
        url = "https://rss.uol.com.br/feed/economia.xml"
        
        try:
            r = httpx.get(url, timeout=10, follow_redirects=True)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, "xml")
            items = soup.find_all("item")
            
            for it in items[:10]:
                title = (it.title.text or "").strip() if it.title else ""
                description = (it.description.text or "").strip() if it.description else ""
                
                # Filtra notícias relevantes
                full_text = f"{title} {description}".lower()
                if company.lower() not in full_text:
                    continue
                
                link = (it.link.text or "").strip() if it.link else ""
                
                published_at = None
                if it.pubDate:
                    try:
                        date_text = it.pubDate.text.strip()
                        dt = datetime.strptime(date_text, "%a, %d %b %Y %H:%M:%S %z")
                        published_at = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        published_at = it.pubDate.text
                
                results.append({
                    "company": company,
                    "title": title,
                    "description": description,
                    "url": link,
                    "fonte": "UOL Economia",
                    "fonte_type": "uol",
                    "published_at": published_at,
                })
            
            print(f"🔵 UOL: {len([r for r in results if r['company']==company])} resultados para {company}")
        except Exception as e:
            print(f"⚠️ Erro ao buscar UOL para {company}: {e}")
    
    return results

# ==============================================================
# 🏢 SITE OFICIAL DA EMPRESA
# ==============================================================

def fetch_company_website_news(companies: List[str]) -> List[Dict[str, str]]:
    """Tenta buscar notícias diretamente do site oficial da empresa"""
    results = []
    
    # Mapeamento de empresas conhecidas para seus feeds RSS/páginas de notícias
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
        "stone": {
            "press": "https://investors.stone.co/news-and-events/",
            "news_page": "https://www.stone.com.br/imprensa/"
        },
        "magazine luiza": {
            "press": "https://ri.magazineluiza.com.br/",
            "news_page": "https://www.magazineluiza.com.br/"
        },
        "mercado livre": {
            "press": "https://www.mercadolivre.com.br/institucional/sala-de-imprensa",
        },
        "natura": {
            "press": "https://www.naturaeco.com.br/sala-de-imprensa/",
        }
    }
    
    for company in companies:
        company_lower = company.lower()
        
        # Verifica se temos URLs mapeadas para esta empresa
        if company_lower not in company_urls:
            print(f"⚠️  Site oficial: Empresa '{company}' não mapeada")
            continue
        
        urls = company_urls[company_lower]
        
        # Tenta buscar RSS primeiro
        if "rss" in urls:
            try:
                r = httpx.get(urls["rss"], timeout=10, follow_redirects=True)
                r.raise_for_status()
                soup = BeautifulSoup(r.content, "xml")
                items = soup.find_all("item")
                
                for it in items[:5]:
                    title = (it.title.text or "").strip() if it.title else ""
                    description = (it.description.text or "").strip() if it.description else ""
                    link = (it.link.text or "").strip() if it.link else ""
                    
                    published_at = None
                    if it.pubDate:
                        try:
                            date_text = it.pubDate.text.strip()
                            dt = datetime.strptime(date_text, "%a, %d %b %Y %H:%M:%S %z")
                            published_at = dt.strftime("%d/%m/%Y %H:%M")
                        except:
                            published_at = it.pubDate.text
                    
                    results.append({
                        "company": company,
                        "title": title,
                        "description": description,
                        "url": link,
                        "fonte": f"{company} Oficial",
                        "fonte_type": "company_website",
                        "published_at": published_at,
                    })
                
                print(f"🏢 {company} (Site Oficial RSS): {len([r for r in results if r['company']==company])} resultados")
                continue
                
            except Exception as e:
                print(f"⚠️  Erro ao buscar RSS de {company}: {e}")
        
        # Se não tiver RSS ou falhar, tenta scraping da página de notícias/imprensa
        news_url = urls.get("press") or urls.get("news_page")
        if news_url:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                }
                r = httpx.get(news_url, headers=headers, timeout=10, follow_redirects=True)
                r.raise_for_status()
                soup = BeautifulSoup(r.content, "html.parser")
                
                # Procura por elementos comuns de notícias
                # Isso varia muito por site, então é uma abordagem genérica
                news_elements = (
                    soup.find_all("article", limit=5) or
                    soup.find_all("div", class_=lambda x: x and ("news" in x.lower() or "post" in x.lower()), limit=5) or
                    soup.find_all("h2", limit=5)
                )
                
                for elem in news_elements:
                    # Tenta extrair título
                    title_tag = elem.find(["h1", "h2", "h3", "a"])
                    if not title_tag:
                        continue
                    
                    title = title_tag.get_text(strip=True)
                    
                    # Tenta extrair link
                    link_tag = elem.find("a", href=True)
                    link = link_tag["href"] if link_tag else news_url
                    
                    # Corrige links relativos
                    if link.startswith("/"):
                        from urllib.parse import urljoin
                        link = urljoin(news_url, link)
                    
                    # Tenta extrair descrição
                    desc_tag = elem.find("p")
                    description = desc_tag.get_text(strip=True)[:200] if desc_tag else ""
                    
                    results.append({
                        "company": company,
                        "title": title,
                        "description": description,
                        "url": link,
                        "fonte": f"{company} Oficial",
                        "fonte_type": "company_website",
                        "published_at": None,
                    })
                
                print(f"🏢 {company} (Site Oficial): {len([r for r in results if r['company']==company])} resultados")
                
            except Exception as e:
                print(f"⚠️  Erro ao buscar site de {company}: {e}")
    
    return results

# ==============================================================
# 🔹 AGREGADOR FINAL
# ==============================================================

def fetch_real_news(companies: List[str]) -> List[Dict[str, str]]:
    """Combina TODAS as fontes de notícias disponíveis e ordena por data"""
    results = []
    
    print(f"\n🚀 Iniciando busca em múltiplas fontes para: {', '.join(companies)}\n")
    
    # 🏢 PRIORIDADE: Site oficial da empresa (fonte mais confiável)
    results.extend(fetch_company_website_news(companies))
    
    # Fontes principais (sempre ativas)
    results.extend(fetch_google_news(companies))
    results.extend(fetch_g1_news(companies))
    results.extend(fetch_infomoney_news(companies))
    results.extend(fetch_uol_news(companies))
    results.extend(fetch_reuters_news(companies))
    results.extend(fetch_yahoo_finance_news(companies))
    results.extend(fetch_duckduckgo_news(companies))
    
    # Fontes com API key (opcionais)
    for company in companies:
        results.extend(fetch_linkedin_posts(company))
    
    if BING_API_KEY:
        results.extend(fetch_bing_news(companies))
    
    print(f"\n✅ Total: {len(results)} notícias encontradas de todas as fontes")
    
    # 📅 ORDENAÇÃO POR DATA (mais recente primeiro)
    results = sort_by_date(results)
    print(f"📅 Notícias ordenadas por data (mais recentes primeiro)\n")
    
    return results


def sort_by_date(news_list: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Ordena lista de notícias por data (mais recente primeiro)"""
    def parse_date(news_item):
        """Converte string de data para datetime para ordenação"""
        published_at = news_item.get("published_at")
        
        if not published_at:
            # Notícias sem data vão para o final
            return datetime.min
        
        try:
            # Formato esperado: "DD/MM/YYYY HH:MM"
            if "/" in published_at and ":" in published_at:
                dt = datetime.strptime(published_at, "%d/%m/%Y %H:%M")
                return dt
            
            # Tenta outros formatos comuns
            for fmt in [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%d/%m/%Y",
                "%Y-%m-%d"
            ]:
                try:
                    return datetime.strptime(published_at, fmt)
                except:
                    continue
            
            # Se não conseguir parsear, coloca no final
            return datetime.min
            
        except Exception as e:
            print(f"⚠️  Erro ao parsear data '{published_at}': {e}")
            return datetime.min
    
    # Ordena por data (mais recente primeiro)
    sorted_news = sorted(news_list, key=parse_date, reverse=True)
    
    return sorted_news
