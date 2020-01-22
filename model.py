from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String, Float


Base = declarative_base()
class Armani(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    product_name = Column(String)
    color = Column(String)
    full_price = Column(Float)
    discount_price = Column(Float)
    product_id = Column(String)
    size = Column(String)
    img_name = Column(String)

    def __init__(self, product_name, color, full_price, discount_price, product_id, size, img_name):
        self.product_name = product_name
        self.color = color
        self.full_price = full_price
        self.discount_price = discount_price
        self.product_id = product_id
        self.size = size
        self.img_name = img_name

    def __repr__(self):
        return "CData '%s'" % (self.url)

db_engine = create_engine("sqlite:///armani.db", echo=True)
Base.metadata.create_all(db_engine)