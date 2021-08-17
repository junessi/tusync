from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select, desc
from data.Daily import Daily
from common.config import read_config
import math
import time
import tushare as ts
import datetime

Base = declarative_base()

class TUData():
    '''
         Database data write, modify
    '''
    def __init__(self):
        config = read_config()
        self.pro = ts.pro_api(config["token"])
        conn_str = "mysql+pymysql://{0}:{1}@{2}/{3}?charset={4}".format(config["mysql_user"],
                                                                        config["mysql_password"],
                                                                        config["mysql_server"],
                                                                        config["mysql_db"],
                                                                        config["mysql_charset"])
        self.engine = create_engine(conn_str, pool_size=64, max_overflow=64)
        self.session = sessionmaker(bind = self.engine, autoflush = False)

    def get_stock_list(self, exchange):
        """
            exchange: SSE->上交所, SZSE->深交所。
        """
        if exchange in ['SSE', 'SZSE']:
            return self.pro.stock_basic(exchange)

        raise BaseException("Invalid exchange code '{0}'".format(exchange))

    def update_daily(self, ts_code = '', trade_date = '', start_dt = '', end_dt = ''):
        retries = 3
        num_updated = 0
        while retries > 0:
            try:
                fields = 'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
                if trade_date:
                    result = self.pro.daily(ts_code=ts_code, trade_date=trade_date, fields = fields)
                else:
                    result = self.pro.daily(ts_code=ts_code, start_date=start_dt, end_date=end_dt, fields = fields)
                session = self.session()
                num_stocks = len(result.ts_code)
                for i in range(0, num_stocks):
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
                                        amount        = None if math.isnan(result.amount[i]) else result.amount[i]))

                session.commit()
                num_updated = num_stocks
                retries = 0
            except Exception as e:
                retries = retries - 1
                print(e)
                time.sleep(10)

        return num_updated

    def get_open_dates(self, exchange, start_date, end_date):
        df = self.pro.trade_cal(exchange = exchange, is_open='1', start_date=start_date, end_date=end_date, fields='cal_date')
        return [date for date in df.cal_date]

    def get_last_updated_date(self, stock_code):
        session = self.session()
        for d in session.query(Daily).filter_by(ts_code = stock_code).order_by(desc(Daily.trade_date)).limit(1):
            return d.trade_date

        return None

