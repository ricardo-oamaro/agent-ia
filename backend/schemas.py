from pydantic import BaseModel, HttpUrl
from typing import Literal

EventType = Literal["Aquisição", "Certificação", "Lançamento de Produto", "Outro"]

class NewsItem(BaseModel):
    empresa: str
    evento: EventType
    resumo: str
    fonte: HttpUrl