from command.State import State
import common.helpers as helpers
from common.constants import DECADES, EXCHANGES
from common.async_updater import AsyncUpdater
from data.TUData import TUData
from datetime import datetime
import time

class UpdateTo:
    def __init__(self, params, exchange, stock_code, from_date):
        self.state = State.NULL
        
        to_date = params.current()
        if (len(to_date) == 0) or (helpers.is_date(to_date) == True):
            # Note: even if to_date is an empty string, we can still pass it forward as if it is not set.
            self.state = self.update_to_date(exchange, stock_code, from_date, to_date)
        else:
            raise BaseException("Unknown from date: '{0}'".format(to_date))

    def get_state(self):
        return self.state

    def update_to_date(self, exchange, stock_code, from_date, to_date):
        td = TUData()
        exchanges = EXCHANGES if exchange == '' else [exchange]
        stock_codes = []

        if stock_code == '':
            for e in exchanges:
                stock_codes = stock_codes + [c[:-3] for c in td.get_stock_list(e).ts_code]
            print("update {0} stocks in exchange {1} from {2} ".format(len(stock_codes), e, from_date))
        else:
            print("update {0} in exchange {1} from {2} ".format(stock_code, exchange, from_date))
            stock_codes.append(stock_code)

        for s in stock_codes:
            for decade in DECADES:
                if int(from_date) > decade['end']:
                    continue

                # print("update {0} in {1} from {2} ".format(s, e, from_date))
                td.update_daily(exchange, stock_code = s, start_date = from_date, end_date = to_date)

        return State.DONE


class UpdateFrom:
    def __init__(self, params, exchange = '', stock_code = ''):
        self.state = State.NULL
        
        from_date = params.next()
        if len(from_date) == 0:
            # no date specified -> update all
            return
        elif helpers.is_date(from_date):
            self.state = UpdateTo(params, exchange, stock_code, from_date).get_state()
        else:
            raise BaseException("Unknown from date: '{0}'".format(from_date))

    def get_state(self):
        return self.state


class UpdateStock:
    def __init__(self, params):
        self.state = State.NULL

        stock_code = params.next()
        self.state = UpdateFrom(params, stock_code).get_state()
        if self.state == State.NULL:
            # stock_code is the last parameter -> update stock_code in complete history
            print("update stock {0}".format(stock_code))
            td = TUData()
            last_date = int(td.get_last_updated_date(stock_code)) + 1
            today = int(datetime.today().strftime("%Y%m%d"))
            if last_date <= today:
                for decade in DECADES:
                    if last_date > decade['end']:
                        continue

                    from_date = "{0}".format(last_date)
                    to_date = "{0}".format(today)
                    td.update_daily(start_date = from_date, end_date = to_date)

    def get_state(self):
        return self.state


class UpdateExchange:
    def __init__(self, params):
        self.state = State.NULL

        exchange = params.next()
        if helpers.is_exchange(exchange):
            param = params.current()
            if helpers.is_date(param) == False:
                # Exchange name is expected to be followed by a date, otherwise return with NULL state.
                return

            self.state = UpdateFrom(params, exchange).get_state()

            if self.state == State.NULL:
                print("update exchange {0}".format(exchange))
                td = TUData()
                for decade in DECADES:
                    from_date = "{0}".format(decade['start'])
                    to_date = "{0}".format(decade['end'])
                    print("update exchange {0} from {1} to {2}".format(exchange, from_date, to_date))
                    td.update_daily(exchange, start_date = from_date, end_date = to_date)

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
            """
            examples:
                param == -1: today
                param == -2: today and yesterday
            """
            self.state = self.update_last_n_days(int(param[1:]))
        elif helpers.is_exchange(param):
            self.state = UpdateExchange(params).get_state()
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
        num_updated = self.update_exchange_on_dates(exchange, open_dates)
        end_time = time.time()
        print("updated {0} stocks in {1} from {2} to {3} took {4} second(s).".format(num_updated,
                                                                                     exchange,
                                                                                     date_from,
                                                                                     date_to,
                                                                                     end_time - start_time))

    def update_exchange_on_dates(self, exchange, dates):
        u = AsyncUpdater()
        num_updated = u.update_all_stocks_on_dates(exchange, dates)

        return num_updated


