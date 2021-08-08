from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select, desc
from data.Daily import Daily
import time
import tushare as ts
import datetime

Base = declarative_base()

class TUData():
    '''
         Database data write, modify
    '''
    def __init__(self):
        self.pro = ts.pro_api('d594093034879d9d4a15983372cd9d503863ae7d9bdc8b09655bc253')
        self.engine = create_engine("mysql+pymysql://tushare:TUshare_pwd0$@localhost/tushare?charset=utf8mb4")
        self.session = sessionmaker(bind = self.engine)

    def get_stock_list(self, exchange):
        """
            exchange: SH->上交所, SZ->深交所。
        """
        if exchange == 'SH':
            return self.pro.stock_basic(exchange = 'SSE')
        elif exchange == 'SZ':
            return self.pro.stock_basic(exchange = 'SZSE')

        raise BaseException("Invalid exchange code '{0}'".format(exchange))

    def update_daily(self, ts_code, start_dt = None, end_dt = None):
        retries = 3
        while retries > 0:
            try:
                fields = 'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
                result = self.pro.daily(ts_code=ts_code, start_date=start_dt, end_date=end_dt, fields = fields)
                session = self.session()
                for i in range(0, len(result.ts_code)):
                    session.merge(Daily(ts_code       = result.ts_code[i],
                                        trade_date    = result.trade_date[i],
                                        open          = result.open[i],
                                        high          = result.high[i],
                                        low           = result.low[i],
                                        close         = result.close[i],
                                        pre_close     = result.pre_close[i],
                                        change        = result.change[i],
                                        pct_chg       = result.pct_chg[i],
                                        vol           = result.vol[i],
                                        amount        = result.amount[i]))

                session.commit()
                retries = 0
            except Exception as e:
                retries = retries - 1
                print(e)
                time.sleep(1)

    def get_last_updated_date(self, stock_code):
        session = self.session()
        for d in session.query(Daily).filter_by(ts_code = stock_code).order_by(desc(Daily.trade_date)).limit(1):
            return d.trade_date

        return None

