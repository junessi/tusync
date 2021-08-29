from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import create_engine, select, desc
from data.Daily import Daily
from common.config import read_config
import math
import queue
import threading
import time
import tushare as ts
import datetime

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
        self.session = sessionmaker(bind = self.engine, autoflush = False)

    def get_stock_list(self, exchange):
        """
             SSE: 上交所
            SZSE: 深交所
        """
        if exchange in ['SSE', 'SZSE']:
            self.wait_for_available_call()

            return self.pro.stock_basic(exchange)

        raise BaseException("Invalid exchange code '{0}'".format(exchange))

    def update_daily(self, ts_code = '', trade_date = '', start_dt = '', end_dt = ''):
        retries = 10 # max retries
        num_updated = 0
        while retries > 0:
            try:
                self.wait_for_available_call()

                fields = 'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
                if trade_date:
                    result = self.pro.daily(ts_code=ts_code, trade_date=trade_date, fields = fields)
                else:
                    result = self.pro.daily(ts_code=ts_code, start_date=start_dt, end_date=end_dt, fields = fields)

                with self.session() as session:
                    num_updated = self.save_dailies(session, result)

                break
            except Exception as e:
                retries = retries - 1
                print("update_daily(): {0}".format(e))
                time.sleep(10)

        if retries == 0:
            print("update_daily(ts_code = '{0}', trade_date = '{1}', start_dt = '{2}', end_dt = '{3}') failed."
                  .format(ts_code, trade_date, start_dt, end_dt))

        return num_updated

    def save_dailies(self, session, result):
        # print(self.engine.pool.status())
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
        return num_stocks

    def get_open_dates(self, exchange, start_date, end_date):
        self.wait_for_available_call()

        df = self.pro.trade_cal(exchange = exchange, is_open='1', start_date=start_date, end_date=end_date, fields='cal_date')
        return [date for date in df.cal_date]

    def get_last_updated_date(self, stock_code):
        with self.session() as session:
            for d in session.query(Daily).filter_by(ts_code = stock_code).order_by(desc(Daily.trade_date)).limit(1):
                return d.trade_date

        return None

    def wait_for_available_call(self):
        try:
            TUData.call_ts_lock.acquire()

            while TUData.call_timestamps.full():
                # remove all time stamps older than TUData.seconds
                sixty_seconds_ago = time.time() - TUData.seconds
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

            TUData.call_timestamps.put(int(time.time()))
        except Exception as e:
            print("wait_for_available_call(): {}".format(e))
        finally:
            TUData.call_ts_lock.release()


