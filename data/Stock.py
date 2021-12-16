from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String

Base = declarative_base()


class StockSSE(Base):
    __tablename__ = 'stock_list_SSE'

    stock_code = Column(String(16), primary_key=True)
    name_cn = Column(String(128))
    name_en = Column(String(128))
    fullname = Column(String(128))
    list_date = Column(String(8))
    delist_date = Column(String(8))

class StockSZSE(Base):
    __tablename__ = 'stock_list_SZSE'

    stock_code = Column(String(16), primary_key=True)
    name_cn = Column(String(128))
    name_en = Column(String(128))
    fullname = Column(String(128))
    list_date = Column(String(8))
    delist_date = Column(String(8))

