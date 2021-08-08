from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,String,Float,Text

Base = declarative_base()

class Daily(Base):
    """ Daily Quotes
     ts_code str N stock code (choose one)
     trade_date str N trade date (choose one)
     start_date str N start date (YYYYMMDD)
     end_date str N End date (YYYYMMDD)
    """

    __tablename__ = 'daily'

    ts_code = Column(String(10), primary_key=True) # Stock code
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

