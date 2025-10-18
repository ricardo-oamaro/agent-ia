from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from schemas import NewsItem
from data_source import fetch_real_news
from analyzer import analyze_text

app = FastAPI(title="Market News Monitor API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/news", response_model=List[NewsItem])
async def get_news(companies: List[str] = Query(...)):
    raw = fetch_real_news(companies)
    out: List[NewsItem] = []
    for item in raw:
        analysis = analyze_text(
            title=item["title"],
            description=item["description"],
            company=item["company"],
            url=item["url"],            # 👈 usa o link REAL
        )
        out.append(NewsItem(
            empresa=analysis.empresa,
            evento=analysis.evento,
            resumo=analysis.resumo,
            fonte=analysis.fonte,       # 👈 schemas.NewsItem espera 'fonte'
        ))
    return out
