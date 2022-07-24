from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Integer

Base = declarative_base()


class MoneyFlowSSE(Base):
    __tablename__ = 'money_flow_SSE'

    stock_code = Column(String(10), primary_key=True)
    trade_date = Column(String(8), primary_key=True)
    buy_sm_vol = Column(Integer)
    buy_sm_amount = Column(Float)
    sell_sm_vol = Column(Integer)
    sell_sm_amount = Column(Float)
    buy_md_vol = Column(Integer)
    buy_md_amount = Column(Float)
    sell_md_vol = Column(Integer)
    sell_md_amount = Column(Float)
    buy_lg_vol = Column(Integer)
    buy_lg_amount = Column(Float)
    sell_lg_vol = Column(Integer)
    sell_lg_amount = Column(Float)
    buy_elg_vol = Column(Integer)
    buy_elg_amount = Column(Float)
    sell_elg_vol = Column(Integer)
    sell_elg_amount = Column(Float)
    net_mf_vol = Column(Integer)
    net_mf_amount = Column(Float)
    trade_count = Column(Integer)


class MoneyFlowSZSE(Base):
    __tablename__ = 'money_flow_SZSE'

    stock_code = Column(String(10), primary_key=True)
    trade_date = Column(String(8), primary_key=True)
    buy_sm_vol = Column(Integer)
    buy_sm_amount = Column(Float)
    sell_sm_vol = Column(Integer)
    sell_sm_amount = Column(Float)
    buy_md_vol = Column(Integer)
    buy_md_amount = Column(Float)
    sell_md_vol = Column(Integer)
    sell_md_amount = Column(Float)
    buy_lg_vol = Column(Integer)
    buy_lg_amount = Column(Float)
    sell_lg_vol = Column(Integer)
    sell_lg_amount = Column(Float)
    buy_elg_vol = Column(Integer)
    buy_elg_amount = Column(Float)
    sell_elg_vol = Column(Integer)
    sell_elg_amount = Column(Float)
    net_mf_vol = Column(Integer)
    net_mf_amount = Column(Float)
    trade_count = Column(Integer)

