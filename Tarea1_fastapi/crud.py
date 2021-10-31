from datetime import date
from sqlalchemy.orm import Session
from . import models,schemas
from  uuid import uuid4 as uuid

"""
    entregar:{
                id:
                tittle
                url
                date:
                media_outlet
                category:
           }
"""

def get_news(db: Session, from1: date,to: date,category: str):
    modNews = models.News
    modHas = models.Has_category
    resp = db.query(modNews).join(modHas).filter(modNews.date.between(from1,to),modHas.value==category).all()
    for valor in resp:
        valor.__setattr__("category",category)
    return resp

def create_news(db: Session,news: schemas.NewsCreate):
    id_news = str(uuid())
    db_news = models.News(id=id_news,title=news.title,date=news.date,url=news.url,media_outlet=news.media_outlet)

    db.add(db_news)
    db.commit()
    db.refresh(db_news)

    for categoria in news.category:
        create_news_category(db=db,valor=categoria,news_id=id_news)

    return db_news

def create_news_category(db:Session,valor: str,news_id:str):
    id_category = str(uuid())
    db_has_category = models.Has_category(id=id_category,value=valor,id_news=news_id)
    db.add(db_has_category)
    db.commit()
    db.refresh(db_has_category)
    return db_has_category

