import os
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict
from dotenv import load_dotenv

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
        try:
            r = httpx.get(url, timeout=10, follow_redirects=True)
            r.raise_for_status()
            soup = _soup_xml(r.content)
            items = soup.find_all("item")

            for it in items[:10]:
                title = (it.title.text or "").strip() if it.title else ""
                link_google = (it.link.text or "").strip() if it.link else ""
                description = (it.description.text or "").strip() if it.description else ""

                article_url = _first_publisher_link(description) or link_google
                if not title or not article_url:
                    continue

                results.append({
                    "company": company,
                    "title": title,
                    "description": description,
                    "url": article_url,
                    "fonte": "Google News",
                    "fonte_type": "google"
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
        for item in data.get("organic_results", []):
            results.append({
                "company": company,
                "title": item.get("title", ""),
                "description": item.get("snippet", ""),
                "url": item.get("link", ""),
                "fonte": "LinkedIn",
                "fonte_type": "linkedin"
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
