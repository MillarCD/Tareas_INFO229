from typing import List, Optional
from pydantic import BaseModel
from datetime import date 


class NewsBase(BaseModel):
    title: str
    date: date
    url: str
    media_outlet: str

class NewsCreate(NewsBase):
    category: List[str]
    pass

class NewsPost(NewsBase):
    class Config:
        orm_mode = True

class News(NewsBase):
    category: str
    class Config:
        orm_mode = True



class Has_category(BaseModel):
    id: str
    value: str
    id_news: str
    class Config:
        orm_mode = True
