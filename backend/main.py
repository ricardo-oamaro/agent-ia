from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from schemas import NewsItem
from data_source import fetch_real_news
from analyzer import analyze_text

app = FastAPI(title="Market News Monitor API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/news", response_model=List[NewsItem])
async def get_news(companies: List[str] = Query(...)):
    raw = fetch_real_news(companies)
    return raw
