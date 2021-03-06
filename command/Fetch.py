from command.State import State
import common.helpers as helpers
from common.constants import EXCHANGES
from data.TUData import TUData


class Exchange():
    def __init__(self, exchange):
        exchange_code = helpers.get_exchange(exchange)
        self.exchange = exchange if exchange_code == '' else exchange_code

    def fetch(self):
        self.fetch_exchange_stock_list()

    def fetch_exchange_stock_list(self):
        TUData().get_stock_list_of_exchange(self.exchange)


class Fetch:
    def __init__(self, params):
        self.state = State.NULL
        
        param = params.current()
        exchanges = []
        if helpers.is_stock_code_subfix(param):
            exchanges.append(param)
        elif param == '':
            exchanges = EXCHANGES
        else:
            raise BaseException("Invalid input: '{0}'".format(param))

        for ex in exchanges:
            Exchange(ex).fetch()

        self.state = State.DONE

    def get_state(self):
        return self.state

