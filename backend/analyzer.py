import re
from dataclasses import dataclass
from pydantic import HttpUrl

EVENT_AQUISICAO = "Aquisição"
EVENT_CERTIFICACAO = "Certificação"
EVENT_LANCAMENTO = "Lançamento de Produto"
EVENT_OUTRO = "Outro"

KEYWORDS = {
    EVENT_AQUISICAO: ["adquire", "compra", "aquisição"],
    EVENT_CERTIFICACAO: ["certificação", "certificado", "PCI", "ISO"],
    EVENT_LANCAMENTO: ["lança", "lançamento", "apresenta", "novo produto"],
}

@dataclass
class Analysis:
    empresa: str
    evento: str
    resumo: str
    fonte: HttpUrl


def _heuristic_event(title: str, description: str) -> str:
    text = f"{title} {description}".lower()
    for event, kws in KEYWORDS.items():
        if any(kw in text for kw in kws):
            return event
    return EVENT_OUTRO


def _truncate(text: str, limit: int = 200) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def analyze_text(title: str, description: str, company: str, url: HttpUrl) -> Analysis:
    """Função principal de análise de notícia."""
    evento = _heuristic_event(title, description)
    resumo = _truncate(f"{title}. {description}")
    return Analysis(company, evento, resumo, url)





# ==============================================================

# import os
# import json
# import httpx
# from typing import Optional

# from pydantic import HttpUrl

# EVENT_AQUISICAO = "Aquisição"
# EVENT_CERTIFICACAO = "Certificação"
# EVENT_LANCAMENTO = "Lançamento de Produto"
# EVENT_OUTRO = "Outro"

# KEYWORDS = {
#     EVENT_AQUISICAO: ["adquire", "adquiriu", "compra", "comprou", "aquisição", "merge", "merger", "acquisition"],
#     EVENT_CERTIFICACAO: ["certificação", "certificado", "PCI", "ISO", "compliance", "conformidade"],
#     EVENT_LANCAMENTO: ["lança", "lançamento", "apresenta", "novo produto", "introduz", "launch"],
# }

# class Analysis:
#     def __init__(self, empresa: str, evento: str, resumo: str, fonte: HttpUrl):
#         self.empresa = empresa
#         self.evento = evento
#         self.resumo = resumo
#         self.fonte = fonte


# def _heuristic_event(title: str, description: str) -> str:
#     text = f"{title} {description}".lower()
#     for event, kws in KEYWORDS.items():
#         if any(kw in text for kw in kws):
#             return event
#     return EVENT_OUTRO


# def _truncate(text: str, limit: int = 200) -> str:
#     text = " ".join(text.split())
#     return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


# async def _openai_summarize_and_classify(title: str, description: str, company: str) -> Optional[Analysis]:
#     """Classifica e resume uma notícia usando GPT-4o, se OPENAI_API_KEY estiver configurada."""
#     api_key = os.getenv("OPENAI_API_KEY")
#     if not api_key:
#         return None

#     try:
#         system_prompt = (
#             "Você é um classificador de notícias corporativas. "
#             "Retorne JSON com os campos 'evento' e 'resumo'. "
#             "Eventos possíveis: Aquisição, Certificação, Lançamento de Produto ou Outro. "
#             "O resumo deve ter no máximo 200 caracteres, em português natural."
#         )
#         user_prompt = (
#             f"Empresa: {company}\n"
#             f"Título: {title}\n"
#             f"Descrição: {description}\n"
#             f"Responda apenas em JSON."
#         )

#         payload = {
#             "model": "gpt-4o-mini",
#             "messages": [
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt},
#             ],
#             "temperature": 0.3,
#         }

#         headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

#         async with httpx.AsyncClient(timeout=20) as client:
#             resp = await client.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers)
#             resp.raise_for_status()
#             data = resp.json()
#             content = data["choices"][0]["message"]["content"].strip()

#         parsed = json.loads(content)
#         evento = parsed.get("evento") or _heuristic_event(title, description)
#         resumo = _truncate(parsed.get("resumo") or f"{title}. {description}")

#         return Analysis(company, evento, resumo, "https://example.com")

#     except Exception as e:
#         print(f"⚠️ Erro na análise via OpenAI: {e}")
#         return None
