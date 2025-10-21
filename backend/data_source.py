import os
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from dotenv import load_dotenv
from datetime import datetime

# 🔹 Carrega variáveis de ambiente (.env)
load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

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
    """Busca notícias via Google News RSS"""
    results: List[Dict[str, str]] = []

    for company in companies:
        url = f"https://news.google.com/rss/search?q={company}&hl=pt-BR&gl=BR&ceid=BR:pt"
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
# 🔹 AGREGADOR FINAL
# ==============================================================

def fetch_real_news(companies: List[str]) -> List[Dict[str, str]]:
    """Combina todas as fontes (Google News + LinkedIn)"""
    results = []
    for company in companies:
        results.extend(fetch_google_news([company]))
        results.extend(fetch_linkedin_posts(company))
    return results
