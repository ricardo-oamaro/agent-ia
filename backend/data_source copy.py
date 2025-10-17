import os
import httpx
import atoma
from bs4 import BeautifulSoup
from typing import List, Dict

# ==============================================================
# 🔹 Leitura das variáveis de ambiente
# ==============================================================

GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

# ==============================================================
# 🔹 Fonte 1 — GNews.io
# ==============================================================

def fetch_gnews(company: str) -> List[Dict[str, str]]:
    results = []
    if not GNEWS_API_KEY:
        return results

    base_url = "https://gnews.io/api/v4/search"
    params = {"q": company, "lang": "pt", "max": 5, "token": GNEWS_API_KEY}

    try:
        r = httpx.get(base_url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        for a in data.get("articles", []):
            results.append({
                "company": company,
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "url": a.get("url", ""),
                "source": "GNews",
            })
    except Exception as e:
        print(f"⚠️ Erro ao buscar GNews para {company}: {e}")
    return results


# ==============================================================
# 🔹 Fonte 2 — SerpApi (substitui o Bing News)
# ==============================================================

def fetch_serpapi(company: str) -> List[Dict[str, str]]:
    results = []
    if not SERP_API_KEY:
        print("⚠️ SERP_API_KEY não configurada. Ignorando busca SerpApi.")
        return results

    base_url = "https://serpapi.com/search.json"
    params = {
        "engine": "bing_news",
        "q": company,
        "api_key": SERP_API_KEY,
        "num": 5,   # 'num' é o parâmetro oficial
        "cc": "BR",
        "hl": "pt",
    }

    try:
        r = httpx.get(base_url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        # Garante compatibilidade com diferentes estruturas de resposta
        articles = data.get("news_results") or data.get("organic_results") or []
        for item in articles:
            results.append({
                "company": company,
                "title": item.get("title", ""),
                "description": item.get("snippet", ""),
                "url": item.get("link") or item.get("url", ""),
                "source": "SerpApi (Bing News)",
            })
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            print("❌ Erro 401 (Unauthorized) — verifique sua SERP_API_KEY.")
        else:
            print(f"⚠️ HTTP error ao buscar via SerpApi ({company}): {e}")
    except Exception as e:
        print(f"⚠️ Erro geral ao buscar via SerpApi ({company}): {e}")

    return results



# ==============================================================
# 🔹 Fonte 3 — RSS públicos
# ==============================================================

def fetch_rss(company: str) -> list[dict[str, str]]:
    results = []
    RSS_FEEDS = [
        "https://www.band.com.br/bandnews-fm/feed/",
        "https://valor.globo.com/rss/ultimas",
        "https://www.estadao.com.br/rss/ultimas/",
        "https://admin.cnnbrasil.com.br/feed/",
        "https://itforum.com.br/feed/",
        "https://exame.com/feed/",
        "https://www.infomoney.com.br/feed/",
        "https://startups.com.br/feed/",
        "https://g1.globo.com/rss/g1/economia/",
        "https://oglobo.globo.com/rss.xml?completo=true",
        "https://forbes.com.br/feed/",
    ]

    for feed_url in RSS_FEEDS:
        try:
            r = httpx.get(feed_url, timeout=10, follow_redirects=True)
            r.raise_for_status()
            feed = atoma.parse_rss_bytes(r.content)

            for item in feed.items[:8]:
                # Trata campos que podem ser string ou objeto
                title = getattr(item.title, "value", item.title)
                description = getattr(item.description, "value", item.description or "")

                # Tenta recuperar o link de diferentes formas possíveis
                link = ""
                if hasattr(item, "link") and item.link:
                    link = item.link
                elif getattr(item, "links", []):
                    link = getattr(item.links[0], "href", "")
                elif hasattr(item, "guid"):
                    guid = getattr(item.guid, "value", "") if hasattr(item.guid, "value") else str(item.guid)
                    if guid.startswith("http"):
                        link = guid

                # Filtra notícias por empresa
                if not title:
                    continue
                if company.lower() not in title.lower() and company.lower() not in description.lower():
                    continue

                results.append({
                    "company": company,
                    "title": str(title).strip(),
                    "description": str(description).strip(),
                    "url": str(link).strip(),
                    "source": getattr(feed.title, "value", "RSS"),
                })

        except Exception as e:
            print(f"⚠️ Erro ao buscar RSS para {company}: {e}")

    return results



# ==============================================================
# 🔹 Fonte 4 — Sites oficiais das empresas
# ==============================================================

COMPANY_SITES = {
    "Nubank": {
        "rss": "https://blog.nubank.com.br/feed/",
        "url": "https://blog.nubank.com.br/"
    },
    "Totvs": {
        "rss": "https://www.totvs.com/blog/feed/",
        "url": "https://www.totvs.com/blog/"
    },
    "Stone": {
        "rss": "https://blog.stone.com.br/feed/",
        "url": "https://blog.stone.com.br/"
    },
}

def scrape_company_site(company: str, url: str) -> List[Dict[str, str]]:
    results = []
    try:
        resp = httpx.get(url, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        for post in soup.select("article h2, h2.entry-title, .post-title, .card__title"):
            title = post.get_text(strip=True)
            link = post.find("a")["href"] if post.find("a") else url
            results.append({
                "company": company,
                "title": title,
                "description": "",
                "url": link if link.startswith("http") else url + link,
                "source": "Site Oficial",
            })
    except Exception as e:
        print(f"⚠️ Erro ao raspar site da {company}: {e}")
    return results


def fetch_company_sites(companies: List[str]) -> List[Dict[str, str]]:
    results = []
    for company in companies:
        site_info = COMPANY_SITES.get(company)
        if not site_info:
            continue

        # 1️⃣ RSS (preferência)
        if site_info.get("rss"):
            try:
                feed = feedparser.parse(site_info["rss"])
                for entry in feed.entries[:5]:
                    results.append({
                        "company": company,
                        "title": entry.title,
                        "description": entry.summary if "summary" in entry else "",
                        "url": entry.link,
                        "source": "Site Oficial (RSS)",
                    })
                continue
            except Exception as e:
                print(f"⚠️ Erro no RSS de {company}: {e}")

        # 2️⃣ Scraping direto (fallback)
        if site_info.get("url"):
            results += scrape_company_site(company, site_info["url"])

    return results


# ==============================================================
# 🔹 Agregador — Combina todas as fontes
# ==============================================================

def fetch_real_news(companies: List[str]) -> List[Dict[str, str]]:
    """Busca notícias reais de múltiplas fontes."""
    results = []

    for company in companies:
        print(f"🔎 Buscando notícias sobre {company}...")

        # results += fetch_gnews(company)
        # results += fetch_serpapi(company)
        results += fetch_rss(company)
        results += fetch_company_sites([company])

    print(f"✅ Coleta finalizada: {len(results)} notícias encontradas.")
    return results
