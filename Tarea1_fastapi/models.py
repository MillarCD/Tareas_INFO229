from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .database import Base #Se importa el objeto Base desde el archivo database.py

""" 
news = (id,title,date,url,media_outlet)
has_category = (value,#id_news)
"""
class News(Base):
    __tablename__ = "news"

    id = Column(String(50),primary_key=True,index=True)
    title = Column(String(50),unique=True,index=True)
    date = Column(Date)
    url = Column(String(200))
    media_outlet = Column(String(100))
    
    categories = relationship("Has_category",back_populates="owner")


class Has_category(Base):
    __tablename__ = "has_category"

    id = Column(String(50),primary_key=True,index=True)
    value = Column(String(50))
    id_news = Column(String(50),ForeignKey("news.id"))

    owner = relationship("News",back_populates="categories")
