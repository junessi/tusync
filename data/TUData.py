from common.config import read_config
from common.constants import EXCHANGES
from data.local.Database import Database
import common.helpers as helpers
import queue
import threading
import time
import tushare

class TUData():

    # limit: 500 call/min
    calls = 500
    seconds = 60

    call_timestamps = queue.Queue(calls)
    call_ts_lock = threading.Lock()

    def __init__(self):
        config = read_config()
        self.pro = tushare.pro_api(config["token"])
        self.database = Database()

    def create_db_session(self):
        return self.database.create_session()

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

                num_updated = self.database.save_dailies(result)
                break
            except BaseException as e:
                print("update_daily(): Exception caught: {0}".format(e))
                print("update_daily(): retries remaining: {0}".format(retries))
                retries = retries - 1
                time.sleep(60)

        if retries == 0:
            print("update_daily(exchange = '{0}', stock_code = '{1}', trade_date = '{2}', start_date = '{3}', end_date = '{4}') failed."
                  .format(stock_code, trade_date, start_date, end_date))

        return num_updated

    def get_open_dates(self, exchange, start_date, end_date):
        self.wait_for_available_call()

        df = self.pro.trade_cal(exchange = exchange, is_open='1', start_date=start_date, end_date=end_date, fields='cal_date')
        return [date for date in df.cal_date]

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
                return

            self.database.save_stock_list_of_exchange(stock_list)
        else:
            print("get_stock_list_of_exchange: unknown exchange {0}".format(exchange))

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


