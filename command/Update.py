from command.State import State
import common.helpers as helpers
from common.constants import DECADES, EXCHANGES
from common.async_updater import AsyncUpdater
from data.TUData import TUData
from datetime import datetime
import time

class UpdateTo:
    def __init__(self, params, stock_code, from_date):
        self.state = State.NULL
        
        to_date = params.current()
        if len(to_date) == 0:
            # no date specified -> update from a specified date to today
            return
        elif is_date(to_date):
            self.state = self.update_to_date(stock_code, from_date, to_date)
        else:
            raise BaseException("Unknown from date: '{0}'".format(to_date))

    def get_state(self):
        return self.state

    def update_to_date(self, stock_code, from_date, to_date):
        td = TUData()
        if stock_code == None:
            for e in EXCHANGES:
                stock_codes = td.get_stock_list(e).ts_code
                print("update {0} stocks in exchange {1} from {2} to {3}".format(len(stock_codes), e, from_date, to_date))
                for s in stock_codes:
                    for decade in DECADES:
                        if int(from_date) > decade['end']:
                            continue

                        print("update {0} from {1} to {2}".format(s, from_date, to_date))
                        td.update_daily(ts_code = s, start_date = from_date, end_date = to_date)
        else:
            print("update {0} from {1} to {2} ".format(stock_code, from_date, to_date))
            td.update_daily(ts_code = stock_code, start_date = from_date, end_date = to_date)

        return State.DONE


class UpdateFrom:
    def __init__(self, params, stock_code = None):
        self.state = State.NULL
        
        from_date = params.next()
        if len(from_date) == 0:
            # no date specified -> update all
            return
        elif is_date(from_date):
            self.state = UpdateTo(params, stock_code, from_date).get_state()
            if self.state == State.NULL:
                self.state = self.update_from_date(stock_code, from_date)
        else:
            raise BaseException("Unknown from date: '{0}'".format(from_date))

    def get_state(self):
        return self.state

    def update_from_date(self, stock_code, from_date):
        td = TUData()
        if stock_code == None:
            exchanges = ['SH', 'SZ']
            for e in exchanges:
                stock_codes = td.get_stock_list(e).ts_code
                print("update {0} stocks in exchange {1} from {2} ".format(len(stock_codes), e, from_date))
                for s in stock_codes:
                    for decade in DECADES:
                        if int(from_date) > decade['end']:
                            continue

                        print("update {0} from {1} ".format(s, from_date))
                        td.update_daily(ts_code = s, start_date = from_date)
        else:
            print("update {0} from {1} ".format(stock_code, from_date))
            td.update_daily(ts_code = stock_code, start_date = from_date)
        return State.DONE


class UpdateStock:
    def __init__(self, params):
        self.state = State.NULL

        stock_code = params.next()
        self.state = UpdateFrom(params, stock_code).get_state()
        if self.state == State.NULL:
            print("update {0}".format(stock_code))
            td = TUData()
            last_date = int(td.get_last_updated_date(stock_code)) + 1
            today = int(datetime.today().strftime("%Y%m%d"))
            if last_date <= today:
                # print("update from {0} to {1}".format(int(last_date) + 1, today))
                for decade in DECADES:
                    if last_date > decade['end']:
                        continue

                    from_date = "{0}".format(last_date)
                    to_date = "{0}".format(today)
                    td.update_daily(ts_code = stock_code, start_date = from_date, end_date = to_date)

    def get_state(self):
        return self.state


class Update:
    def __init__(self, params):
        self.state = State.NULL
        
        param = params.current()
        if helpers.is_stock_code(param):
            self.state = UpdateStock(params).get_state()
        elif helpers.is_date(param):
            self.state = UpdateFrom(params).get_state()
        elif helpers.is_year(param):
            self.state = self.update_all_in_year(param)
        elif param == 'full':
            self.state = self.update_full()
        elif param == 'today' or len(param) == 0:
            self.state = self.update_last_n_days(1)
        elif helpers.is_negative_number(param):
            self.state = self.update_last_n_days(int(param[1:]))
        else:
            raise BaseException("Invalid input: '{0}'".format(param))

    def get_state(self):
        return self.state

    def update_full(self):
        """
            update all stocks in all exchanges in history
            SSE opened on 19901219
            SZSE opened on 19901201
        """
        today = int(datetime.today().strftime("%Y%m%d"))
        for exchange in EXCHANGES:
            for decade in DECADES:
                for year in decade['years']:
                    self.update_all_in_year(year)

    def update_all_in_year(self, year):
        today = datetime.today().strftime("%Y%m%d")
        date_from = "{0}0101".format(year)
        date_to = "{0}1231".format(year)
        if int(date_from) > int(today):
            return
        if int(date_to) > int(today):
            date_to = today
        for exchange in EXCHANGES:
            self.update_exchange_on_date_range(exchange, date_from, date_to)

    def update_last_n_days(self, n):
        """
            update stocks in all exchanges in last n days, include today
            examples:
                n == 1: today
                n == 2: today and yesterday
                ...
        """
        today = datetime.today().strftime("%Y%m%d")
        date_from = "{0}".format(int(today) - (n - 1))
        date_to = "{0}".format(today)
        for exchange in EXCHANGES:
            self.update_exchange_on_date_range(exchange, date_from, date_to)

    def update_exchange_on_date_range(self, exchange, date_from, date_to):
        td = TUData()
        start_time = time.time()
        open_dates = td.get_open_dates(exchange, date_from, date_to)
        num_updated = self.update_exchange_on_dates(open_dates)
        end_time = time.time()
        print("updated {0} stocks at {1} from {2}, to {3}, took {4} second(s).".format(num_updated,
                                                                                       exchange,
                                                                                       date_from,
                                                                                       date_to,
                                                                                       end_time - start_time))

    def update_exchange_on_dates(self, dates):
        return AsyncUpdater().update_all_stocks_on_dates(dates)

