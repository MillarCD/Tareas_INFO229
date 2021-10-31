from typing import List
from datetime import date

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Ejemplo: GET /v1/news?from=2021-01-01&to=2021-01-31&category=sport
@app.get("/v1/news",response_model=List[schemas.News])
def get_news(from1: date,to: date,category: str, db: Session=Depends(get_db)):
    news = crud.get_news(db=db,from1=from1,to=to,category=category)
    return news

@app.post("/news/",response_model=schemas.NewsPost)
def create_news(news: schemas.NewsCreate, db: Session=Depends(get_db)):
    return crud.create_news(db=db,news=news)
