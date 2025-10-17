import httpx
from bs4 import BeautifulSoup
from typing import List, Dict

def _soup_xml(xml_bytes):
    # tenta XML (requer lxml); se faltar, cai pro parser nativo
    try:
        return BeautifulSoup(xml_bytes, "xml")
    except Exception:
        return BeautifulSoup(xml_bytes, "html.parser")

def _first_publisher_link(description_html: str) -> str:
    try:
        soup = BeautifulSoup(description_html or "", "html.parser")
        a = soup.find("a", href=True)
        return a["href"].strip() if a else ""
    except Exception:
        return ""

def fetch_real_news(companies: List[str]) -> List[Dict[str, str]]:
    """
    Busca notícias reais via Google News RSS, de forma simples.
    Retorna itens com keys: company, title, description, url
    """
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

                # Pega o link REAL do publisher dentro da descrição
                article_url = _first_publisher_link(description) or link_google
                if not title or not article_url:
                    continue

                results.append({
                    "company": company,
                    "title": title,
                    "description": description,
                    "url": article_url,
                })
        except Exception as e:
            print(f"⚠️ Erro ao buscar Google News para {company}: {e}")

    print(f"✅ Coleta finalizada: {len(results)} notícias encontradas.")
    return results


# ==============================================================
# 🔹 Agregador — Combina todas as fontes
# ==============================================================

# def fetch_real_news(companies: list[str]) -> list[dict[str, str]]:
#     """Busca notícias reais de múltiplas fontes."""
#     results = []

#     for company in companies:
#         print(f"🔎 Buscando notícias sobre {company}...")

        
#         results += fetch_google_news(company)

#     print(f"✅ Coleta finalizada: {len(results)} notícias encontradas.")
#     return results