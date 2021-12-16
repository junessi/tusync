from common.config import read_config
from data.local.table.Daily import DailySSE, DailySZSE
from data.local.table.Stock import StockSSE, StockSZSE
from sqlalchemy import create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import math

Base = declarative_base()

class Database:
    def __init__(self):
        config = read_config()
        conn_str = "mysql+pymysql://{0}:{1}@{2}/{3}?charset={4}".format(config["mysql_user"],
                                                                        config["mysql_password"],
                                                                        config["mysql_server"],
                                                                        config["mysql_db"],
                                                                        config["mysql_charset"])
        self.engine = create_engine(conn_str,
                                    # pool_size = 500,
                                    # max_overflow = 20
                                    poolclass = NullPool)

        self.session_factory = sessionmaker(bind = self.engine, autoflush = False)

    def create_session(self):
        return self.session_factory()

    def get_last_updated_date(self, exchange, stock_code):
        with self.create_session() as session:
            if exchange == 'SSE':
                for d in session.query(DailySSE).filter_by(ts_code = stock_code).order_by(desc(DailySSE.trade_date)).limit(1):
                    return d.trade_date
            elif exchange == 'SZSE':
                for d in session.query(DailySZSE).filter_by(ts_code = stock_code).order_by(desc(DailySZSE.trade_date)).limit(1):
                    return d.trade_date

        return None

    def save_dailies(self, result):
        session = self.create_session()
        num_stocks = len(result.ts_code)

        try:
            for i in range(0, num_stocks):
                stock_code = result.ts_code[i]
                daily = None
                if stock_code.endswith('.SH'):
                    daily = DailySSE(stock_code    = stock_code[:-3],
                                     trade_date    = result.trade_date[i],
                                     open          = result.open[i],
                                     high          = result.high[i],
                                     low           = result.low[i],
                                     close         = result.close[i],
                                     pre_close     = result.pre_close[i],
                                     change        = result.change[i],
                                     pct_chg       = result.pct_chg[i],
                                     vol           = result.vol[i],
                                     amount        = None if math.isnan(result.amount[i]) else result.amount[i])
                elif stock_code.endswith('.SZ'):
                    daily = DailySZSE(stock_code    = stock_code[:-3],
                                      trade_date    = result.trade_date[i],
                                      open          = result.open[i],
                                      high          = result.high[i],
                                      low           = result.low[i],
                                      close         = result.close[i],
                                      pre_close     = result.pre_close[i],
                                      change        = result.change[i],
                                      pct_chg       = result.pct_chg[i],
                                      vol           = result.vol[i],
                                      amount        = None if math.isnan(result.amount[i]) else result.amount[i])
                else:
                    continue # ignore this stock code

                # This merge() does not seem to be asynchronous between threads, fix it later.
                session.merge(daily)
        except Exception as e:
            print("save_dailies: caught exception: {0}".format(e))
            session.rollback()
        finally:
            # print("start commit")
            session.commit()
        # print("finished saving {0} stocks in to database".format(num_stocks))

        return num_stocks

    def save_stock_list_of_exchange(self, stock_list):
        session = self.create_session()
        num_stocks = len(stock_list)

        try:
            for i in range(0, num_stocks):
                exchange = stock_list[i]['exchange']
                stock = None
                if exchange == 'SSE':
                    stock = StockSSE(stock_code    = stock_list[i]['stock_code'],
                                     name_cn       = stock_list[i]['name_cn'],
                                     name_en       = stock_list[i]['name_en'],
                                     fullname      = stock_list[i]['fullname'],
                                     list_date     = stock_list[i]['list_date'],
                                     delist_date   = stock_list[i]['delist_date'])
                elif exchange == 'SZSE':
                    stock = StockSZSE(stock_code    = stock_list[i]['stock_code'],
                                      name_cn       = stock_list[i]['name_cn'],
                                      name_en       = stock_list[i]['name_en'],
                                      fullname      = stock_list[i]['fullname'],
                                      list_date     = stock_list[i]['list_date'],
                                      delist_date   = stock_list[i]['delist_date'])
                else:
                    continue # unknow exchange, ignore this stock

                # This merge() does not seem to be asynchronous between threads, fix it later.
                session.merge(stock)
        except Exception as e:
            print("save_stock_list_of_exchange: caught exception: {0}".format(e))
            session.rollback()
        finally:
            session.commit()
