from command.State import State
from common.helpers import is_date, is_stock_code, is_year
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
        if is_stock_code(param):
            self.state = UpdateStock(params).get_state()
        elif is_date(param):
            self.state = UpdateFrom(params).get_state()
        elif is_year(param):
            self.state = self.update_all_in_year(param)
        elif len(param) == 0:
            self.state = self.update_all()
        else:
            raise BaseException("Invalid stock code or date: '{0}'".format(param))

    def get_state(self):
        return self.state

    def update_all(self):
        td = TUData()
        today = int(datetime.today().strftime("%Y%m%d"))
        for exchange in EXCHANGES:
            for decade in DECADES:
                for y in range(0, 10):
                    year_start = decade["start"] + y * 10000
                    year_end   = decade["end"] - (90000 - y * 10000)
                    if year_start > today:
                        break
                    if year_end > today:
                        year_end = today

                    start_time = time.time()
                    open_dates = td.get_open_dates(exchange, str(year_start), str(year_end))
                    AsyncUpdater().update_all_stocks_on_dates(open_dates)
                    end_time = time.time()
                    print("updated stocks at {0} between {1} and {2}, took {3} second(s).".format(exchange,
                                                                                                  year_start,
                                                                                                  year_end,
                                                                                                  end_time - start_time))

    def update_all_in_year(self, year):
        td = TUData()
        today = datetime.today().strftime("%Y%m%d")
        year_start = "{0}0101".format(year)
        year_end = "{0}1231".format(year)
        if int(year_start) > int(today):
            return
        if int(year_end) > int(today):
            year_end = today
        for exchange in EXCHANGES:
            start_time = time.time()
            open_dates = td.get_open_dates(exchange, year_start, year_end)
            num_updated = AsyncUpdater().update_all_stocks_on_dates(open_dates)
            end_time = time.time()
            print("updated {0} stocks at {1} between {2} and {3}, took {4} second(s).".format(num_updated,
                                                                                              exchange,
                                                                                              year_start,
                                                                                              year_end,
                                                                                              end_time - start_time))

