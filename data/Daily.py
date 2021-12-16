from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float

Base = declarative_base()


class DailySSE(Base):
    __tablename__ = 'daily_SSE'

    stock_code = Column(String(10), primary_key=True) # stock code
    trade_date = Column(String(8), primary_key=True) # trade date
    open = Column(Float) # opening price
    high = Column(Float) # highest price
    low = Column(Float) # lowest price
    close = Column(Float) # closing price
    pre_close = Column(Float) # Price closed yesterday
    change = Column(Float) # change amount
    pct_chg = Column(Float) # fluctuations (without reinstatement, if it is reinstatement, please use the general market interface)
    vol = Column(Float) # volume (hands)
    amount = Column(Float) # turnover (thousand yuan)

class DailySZSE(Base):
    __tablename__ = 'daily_SZSE'

    stock_code = Column(String(10), primary_key=True) # stock code
    trade_date = Column(String(8), primary_key=True) # trade date
    open = Column(Float) # opening price
    high = Column(Float) # highest price
    low = Column(Float) # lowest price
    close = Column(Float) # closing price
    pre_close = Column(Float) # Price closed yesterday
    change = Column(Float) # change amount
    pct_chg = Column(Float) # fluctuations (without reinstatement, if it is reinstatement, please use the general market interface)
    vol = Column(Float) # volume (hands)
    amount = Column(Float) # turnover (thousand yuan)
