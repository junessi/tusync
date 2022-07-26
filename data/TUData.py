from common.config import read_config
from common.constants import EXCHANGES
from data.local.Database import Database
import queue
import threading
import time
import tushare

class TUData():

    # limit: 500 calls/min
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

    def update_daily(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        """
            handling priority:
                [exchange, stock_code, trade_date]:           update stock_code on trade_date in exchange
                [exchange, stock_code, start_date, end_date]: update stock_code from start_date to end_date in exchange
        """
        max_retries = 10 # max retries
        retry = 1
        num_updated = 0
        while retry <= max_retries:
            try:
                self.wait_for_available_call()
                print("update_daily(exchange = '{0}', stock_code = '{1}', trade_date = '{2}', start_date = '{3}', end_date = '{4}')."
                      .format(exchange, stock_code, trade_date, start_date, end_date))

                fields = 'ts_code,trade_date,open,high,low,close,pre_close,change,pct_chg,vol,amount'
                ts_code = "{0}.{1}".format(stock_code, exchange)

                if trade_date:
                    result = self.pro.daily(ts_code = ts_code,
                                            trade_date = trade_date,
                                            fields = fields)
                else:
                    result = self.pro.daily(ts_code = ts_code,
                                            start_date = start_date,
                                            end_date = end_date,
                                            fields = fields)

                num_updated = self.database.save_dailies(result)
                break
            except BaseException as e:
                print("update_daily(): Exception caught: {0}".format(e))
                print("update_daily(): retry: {0}".format(retry))
                retry = retry + 1
                time.sleep(60)

        if retry == max_retries:
            print("update_daily() failed, max retries reached.")

        return num_updated

    def update_money_flow(self, exchange, stock_code, start_date, end_date):
        max_retries = 10 # max retries
        retry = 1
        num_updated = 0
        while retry <= max_retries:
            try:
                self.wait_for_available_call()
                print("update_money_flow(exchange = '{0}', stock_code = '{1}', start_date = '{2}', end_date = '{3}')."
                      .format(exchange, stock_code, start_date, end_date))

                fields = 'ts_code, trade_date, buy_sm_vol, buy_sm_amount, sell_sm_vol, sell_sm_amount, buy_md_vol,' \
                         'buy_md_amount, sell_md_vol, sell_md_amount, buy_lg_vol, buy_lg_amount, sell_lg_vol, sell_lg_amount,' \
                         'buy_elg_vol, buy_elg_amount, sell_elg_vol, sell_elg_amount, net_mf_vol, net_mf_amount, trade_count'
                ts_code = "{0}.{1}".format(stock_code, exchange)

                result = self.pro.moneyflow(ts_code = ts_code,
                                            start_date = start_date,
                                            end_date = end_date,
                                            fields = fields)

                num_updated = self.database.save_money_flow(result)
                break
            except BaseException as e:
                print("update_money_flow(): Exception caught: {0}".format(e))
                print("update_money_flow(): retry: {0}".format(retry))
                retry = retry + 1
                time.sleep(60)

        if retry == max_retries:
            print("update_money_flow() failed, max retries reached.")

        return num_updated

    def get_open_dates(self, exchange, start_date, end_date):
        self.wait_for_available_call()

        df = self.pro.trade_cal(exchange = exchange, is_open='1', start_date=start_date, end_date=end_date, fields='cal_date')
        return [date for date in df.cal_date]

    def get_stock_list_of_exchange(self, exchange):
        print("fetch stock list of {0}".format(exchange))
        if exchange in EXCHANGES:
            try:
                fields = 'exchange,symbol,name,enname,fullname,list_date,delist_date,industry,area'
                result = self.pro.stock_basic(exchange = exchange, fields = fields)
                stock_list = []
                for i in range(0, len(result.symbol)):
                    stock_list.append({'exchange': result.exchange[i],
                                       'stock_code': result.symbol[i],
                                       'name_cn': result.name[i],
                                       'name_en': result.enname[i],
                                       'fullname': result.fullname[i],
                                       'list_date': result.list_date[i],
                                       'delist_date': result.delist_date[i],
                                       'industry': result.industry[i],
                                       'area': result.area[i]})

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

                time.sleep(2) # queue is still full, take a short break before next check.

            t = int(time.time())
            TUData.call_timestamps.put(t)
        except Exception as e:
            print("wait_for_available_call(): {}".format(e))
        finally:
            TUData.call_ts_lock.release()


