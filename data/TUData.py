from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine, desc
from common.constants import EXCHANGES
from data.Daily import DailySSE, DailySZSE
from data.Stock import StockSSE, StockSZSE
from common.config import read_config
import common.helpers as helpers
import math
import queue
import threading
import time
import tushare as ts

Base = declarative_base()

class TUData():

    # limit: 500 call/min
    calls = 500
    seconds = 60

    call_timestamps = queue.Queue(calls)
    call_ts_lock = threading.Lock()

    def __init__(self):
        config = read_config()
        self.pro = ts.pro_api(config["token"])
        conn_str = "mysql+pymysql://{0}:{1}@{2}/{3}?charset={4}".format(config["mysql_user"],
                                                                        config["mysql_password"],
                                                                        config["mysql_server"],
                                                                        config["mysql_db"],
                                                                        config["mysql_charset"])
        self.engine = create_engine(conn_str,
                                    # pool_size = 500,
                                    # max_overflow = 20
                                    poolclass = NullPool
                                    )

        self.session_factory = sessionmaker(bind = self.engine, autoflush = False)

    def get_db_session(self):
        return self.session_factory()

    def get_stock_list(self, exchange):
        """
             SSE: 上交所
            SZSE: 深交所
        """
        if exchange in EXCHANGES:
            self.wait_for_available_call()

            return self.pro.stock_basic(exchange = exchange)

        raise Exception("Invalid exchange code '{0}'".format(exchange))

    def update_daily(self, exchange = '', stock_code = '', trade_date = '', start_date = '', end_date = ''):
        retries = 10 # max retries
        num_updated = 0
        while retries > 0:
            try:
                self.wait_for_available_call()

                fields = 'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
                if trade_date:
                    result = self.pro.daily(trade_date = trade_date, fields = fields)
                else:
                    if stock_code:
                        stock_code = "{0}.{1}".format(stock_code, helpers.get_stock_code_ending(exchange))

                    result = self.pro.daily(ts_code = stock_code,
                                            start_date = start_date,
                                            end_date = end_date,
                                            fields = fields)

                num_updated = self.save_dailies(result)
                break
            except Exception as e:
                retries = retries - 1
                print("update_daily(): {0}".format(e))
                time.sleep(10)

        if retries == 0:
            print("update_daily(exchange = '{0}', stock_code = '{1}', trade_date = '{2}', start_date = '{3}', end_date = '{4}') failed."
                  .format(stock_code, trade_date, start_date, end_date))

        return num_updated

    def save_dailies(self, result):
        session = self.get_db_session()
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

    def get_open_dates(self, exchange, start_date, end_date):
        self.wait_for_available_call()

        df = self.pro.trade_cal(exchange = exchange, is_open='1', start_date=start_date, end_date=end_date, fields='cal_date')
        return [date for date in df.cal_date]

    def get_last_updated_date(self, exchange, stock_code):
        with self.get_db_session() as session:
            if exchange == 'SSE':
                for d in session.query(DailySSE).filter_by(ts_code = stock_code).order_by(desc(DailySSE.trade_date)).limit(1):
                    return d.trade_date
            elif exchange == 'SZSE':
                for d in session.query(DailySZSE).filter_by(ts_code = stock_code).order_by(desc(DailySZSE.trade_date)).limit(1):
                    return d.trade_date

        return None

    def get_stock_list_of_exchange(self, exchange):
        if exchange in EXCHANGES:
            try:
                fields = 'exchange,symbol,name,enname,fullname,list_date,delist_date'
                result = self.pro.stock_basic(exchange = exchange, fields = fields)
                stock_list = []
                for i in range(0, len(result.symbol)):
                    stock_list.append({'exchange': result.exchange[i],
                                       'stock_code': result.symbol[i],
                                       'name_cn': result.name[i],
                                       'name_en': result.enname[i],
                                       'fullname': result.fullname[i],
                                       'list_date': result.list_date[i],
                                       'delist_date': result.delist_date[i]})

            except BaseException as e:
                print("get_stock_list_of_exchange: exception caught: {0}".format(e))
            finally:
                self.save_stock_list_of_exchange(stock_list)
        else:
            print("get_stock_list_of_exchange: unknown exchange {0}".format(exchange))

    def save_stock_list_of_exchange(self, stock_list):
        session = self.get_db_session()
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

    def wait_for_available_call(self):
        try:
            TUData.call_ts_lock.acquire()

            while TUData.call_timestamps.full():
                # remove all time stamps older than TUData.seconds
                sixty_seconds_ago = int(time.time() - TUData.seconds)
                timestamps_list = list(TUData.call_timestamps.queue)
                n = len(timestamps_list)
                # print("timestamps queue size: {0}".format(n))
                for i in range(n):
                    t = timestamps_list[i]
                    if t < sixty_seconds_ago:
                        ts = TUData.call_timestamps.get()
                        # print("remove {0}".format(ts))
                        TUData.call_timestamps.task_done()
                    else:
                        # print("{0} calls in last 60s".format(TUData.call_timestamps.qsize()))
                        break

                if TUData.call_timestamps.full() == False:
                    break

                time.sleep(1)

            t = int(time.time())
            TUData.call_timestamps.put(t)
        except Exception as e:
            print("wait_for_available_call(): {}".format(e))
        finally:
            TUData.call_ts_lock.release()


