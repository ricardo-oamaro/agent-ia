from pydantic import BaseModel, HttpUrl
from typing import Literal
from typing import Optional

EventType = Literal["Aquisição", "Certificação", "Lançamento de Produto", "Outro"]

class NewsItem(BaseModel):
    company: str
    title: str
    description: Optional[str] = ""
    url: str
    fonte: str  # Nome da fonte legível
    fonte_type: str 
    published_at: Optional[str] = None