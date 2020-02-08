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
    img_name = Column(String)
    size_list = Column(String)
    color_list = Column(String)
    details_list = Column(String)
    cat_name = Column(String)
    url = Column(String)

    def __init__(self, product_name, color, full_price, discount_price, product_id, img_name, size_list,
                 color_list, details_list, cat_name, url):
        self.product_name = product_name
        self.color = color
        self.full_price = full_price
        self.discount_price = discount_price
        self.product_id = product_id
        self.img_name = img_name
        self.size_list = size_list
        self.color_list = color_list
        self.details_list = details_list
        self.cat_name = cat_name
        self.url = url

    def __repr__(self):
        return "CData '%s'" % (self.url)

class ArmaniPrice(Base):
    __tablename__ = 'price_product'
    id = Column(Integer, primary_key=True)
    color = Column(String)
    full_price = Column(Float)
    discount_price = Column(Float)
    product_id = Column(String)

    def __init__(self, color, full_price, discount_price, product_id):
        self.color = color
        self.full_price = full_price
        self.discount_price = discount_price
        self.product_id = product_id
    def __repr__(self):
        return "CData '%s'" % (self.url)

db_engine = create_engine("sqlite:///armani.db", echo=True)
Base.metadata.create_all(db_engine)
