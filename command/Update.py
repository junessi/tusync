import common.helpers as helpers
import time
from command.State import State
from common.constants import DECADES, EXCHANGES
from common.AsyncTaskExecutor import AsyncTaskExecutor, Task
from data.TUData import TUData
from data.local.Database import Database
from datetime import datetime

class UpdateTo:
    def __init__(self, params, exchange, stock_code, from_date):
        self.state = State.NULL
        
        to_date = params.current()
        if to_date == '':
            # no end date specified
            pass
        elif helpers.is_date(to_date) == True:
            self.state = self.update_to_date(exchange, stock_code, from_date, to_date)
        else:
            raise BaseException("Unknown from date: '{0}'".format(to_date))

    def get_state(self):
        return self.state

    def update_to_date(self, exchange, stock_code, from_date, to_date):
        td = TUData()
        exchanges = EXCHANGES if exchange == '' else [helpers.get_exchange(exchange)]
        stock_codes = []

        if stock_code == '':
            for e in exchanges:
                for c in td.get_stock_list(e).ts_code:
                    stock_codes.append(c.split('.'))
                print("update {0} stocks in exchange {1} from {2} to {3}".format(len(stock_codes), e, from_date, to_date))
        else:
            print("update {0} in exchange {1} from {2} to {3}".format(stock_code, exchange, from_date, to_date))
            stock_codes.append([stock_code, exchange])

        a = AsyncTaskExecutor(64)

        start_time = time.time()
        for c, e in stock_codes:
            for decade in DECADES:
                if int(from_date) > decade['end']:
                    continue

                if int(to_date) < decade['start']:
                    break

                a.push(Task(td.update_daily, e, c, '', from_date, to_date))
                a.push(Task(td.update_money_flow, e, c, from_date, to_date))

        a.execute()
        end_time = time.time()
        print("updated {0} stocks in {1} from {2} took {3} second(s).".format(len(stock_codes),
                                                                              ",".join(exchanges),
                                                                              from_date,
                                                                              end_time - start_time))

        return State.DONE


class UpdateFrom:
    def __init__(self, params, exchange = '', stock_code = ''):
        self.state = State.NULL
        
        param = params.next()
        if param == '':
            return
        elif helpers.is_date(param):
            self.state = UpdateTo(params, exchange, stock_code, param).get_state()
            if self.state == State.NULL:
                self.update_from_date(exchange, stock_code, param)
                self.state = State.DONE
        elif helpers.is_year(param):
            params.add(str(helpers.get_last_date_of_year(param)))
            self.state = UpdateTo(params,
                                  exchange,
                                  stock_code,
                                  str(helpers.get_first_date_of_year(param))).get_state()
        else:
            raise BaseException("UpdateFrom: invalid parameter '{0}'".format(param))

    def get_state(self):
        return self.state

    def update_from_date(self, exchange, stock_code, from_date):
        td = TUData()
        a = AsyncTaskExecutor(64)

        start_time = time.time()
        exchanges = EXCHANGES if exchange == '' else [helpers.get_exchange(exchange)]
        stock_codes = []

        if stock_code == '':
            for e in exchanges:
                for c in td.get_stock_list(e).ts_code:
                    stock_codes.append(c.split('.'))
                print("update {0} stocks in exchange {1} from {2}".format(len(stock_codes), e, from_date))
        else:
            print("update {0} in exchange {1} from {2}".format(stock_code, exchange, from_date))
            stock_codes.append([stock_code, exchange])

        for c, e in stock_codes:
            for decade in DECADES:
                if int(from_date) > decade['end']:
                    continue

                a.push(Task(td.update_daily, e, c, '', from_date, ''))
                a.push(Task(td.update_money_flow, e, c, from_date, ''))

        a.execute()
        end_time = time.time()

        print("updated {0} stocks in {1} from {2} took {3} second(s).".format(len(stock_codes),
                                                                              ",".join(exchanges),
                                                                              from_date,
                                                                              end_time - start_time))

        return State.DONE


class UpdateStock:
    def __init__(self, params):
        self.state = State.NULL

        # stock code format must be checked before this constructor has been called.
        # example: 123456.XX
        #   123456: stock code
        #   XX: exchange subfix
        [stock_code, exchange] = params.next().split('.')
        self.state = UpdateFrom(params, exchange, stock_code).get_state()
        if self.state == State.NULL:
            # stock_code is the last parameter -> update stock_code from last updated date
            # print("update stock {0}.{1}".format(stock_code, exchange))
            db = Database()
            last_date = int(db.get_last_updated_date(exchange, stock_code)) + 1
            today = int(datetime.today().strftime("%Y%m%d"))
            if last_date <= today:
                td = TUData()
                a = AsyncTaskExecutor(64)

                start_time = time.time()
                for decade in DECADES:
                    if last_date > decade['end']:
                        continue

                    from_date = last_date if last_date > decade['start'] else decade['start']
                    to_date = today if today < decade['end'] else decade['end']
                    a.push(Task(td.update_daily, exchange, stock_code, '', str(from_date), str(to_date)))
                    a.push(Task(td.update_money_flow, exchange, stock_code, str(from_date), str(to_date)))
                    last_date = to_date + 1

                a.execute()
                end_time = time.time()
                print("updated 1 stock in exchange {0} from {1} took {2} second(s)".format(exchange,
                                                                                           last_date + 1,
                                                                                           end_time - start_time))

            self.state = State.DONE

    def get_state(self):
        return self.state


class UpdateExchange:
    def __init__(self, params):
        self.state = State.NULL

        exchange = params.next()
        if helpers.is_stock_code_subfix(exchange):
            param = params.current()
            if helpers.is_date(param):
                self.state = UpdateFrom(params, exchange).get_state()

            elif len(param) == 0:
                stock_codes = [c.split('.')[0] for c in td.get_stock_list(exchange).ts_code]
                td = TUData()
                a = AsyncTaskExecutor(64)

                start_time = time.time()
                for stock_code in stock_codes:
                    for decade in DECADES:
                        from_date = "{0}".format(decade['start'])
                        to_date = "{0}".format(decade['end'])
                        a.push(Task(td.update_daily, exchange, stock_code, '', from_date, to_date))
                        a.push(Task(td.update_money_flow, exchange, stock_code, from_date, to_date))
                end_time = time.time()
                print("updated {0} stocks in exchange {1} since opening took {2} second(s)".format(len(stock_codes),
                                                                                                   exchange,
                                                                                                   end_time - start_time))

            else:
                # Exchange name is expected to be followed by a date
                self.state = State.INVALID_DATE

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
        elif param == 'today' or param == '':
            self.state = self.update_last_n_days(1)
        elif helpers.is_negative_number(param):
            """
            examples:
                param == -1: today
                param == -2: today and yesterday
            """
            self.state = self.update_last_n_days(int(param[1:]))
        elif helpers.is_stock_code_subfix(param):
            self.state = UpdateExchange(params).get_state()
        else:
            raise BaseException("Update: Invalid input '{0}'".format(param))

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

        return State.DONE

    def update_all_in_year(self, year):
        today = datetime.today().strftime("%Y%m%d")
        date_from = "{0}0101".format(year)
        date_to = "{0}1231".format(year)
        if int(date_from) > int(today):
            return
        if int(date_to) > int(today):
            date_to = today
        for exchange in EXCHANGES:
            self.update_exchange_in_date_range(exchange, date_from, date_to)

        return State.DONE

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
            self.update_exchange_in_date_range(exchange, date_from, date_to)

        return State.DONE

    def update_exchange_in_date_range(self, exchange, date_from, date_to):
        td = TUData()
        start_time = time.time()
        stock_codes = [c.split('.')[0] for c in td.get_stock_list(exchange).ts_code]
        
        # Use AsyncTaskExecutor to call a bulk of update_daily()
        a = AsyncTaskExecutor(64)
        for stock_code in stock_codes:
            # td.update_daily(exchange, stock_code, start_date = date_from, end_date = date_to)
            a.push(Task(td.update_daily, exchange, stock_code, '', date_from, date_to))
            a.push(Task(td.update_money_flow, exchange, stock_code, date_from, date_to))
        a.execute()
        end_time = time.time()
        print("updated {0} stocks in {1} from {2} to {3} took {4} second(s).".format(len(stock_codes),
                                                                                     exchange,
                                                                                     date_from,
                                                                                     date_to,
                                                                                     end_time - start_time))
