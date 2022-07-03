from datetime import datetime
import unittest

from command.Command import Command
from command.State import State
from command.Parameters import Parameters
from data.TUData import TUData
from unittest.mock import patch


class testFetch(unittest.TestCase):
    def setUp(self):
        self.stock_list = list()

    def init_TUData(self):
        pass

    def get_stock_list_of_exchange_mock(self, exchange):
        print("exchange: {0}".format(exchange))
        if exchange == "SSE":
            self.stock_list.extend(["500001.SH", "500002.SH", "500003.SH"])
        elif exchange == "SZSE":
            self.stock_list.extend(["500004.SZ", "500005.SZ", "500006.SZ"])

    def test_fetch_exchange(self):
        self.stock_list = list()
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'get_stock_list_of_exchange', new = self.get_stock_list_of_exchange_mock):

            cmd = Command(Parameters(['fetch', 'SH']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.stock_list, ["500001.SH", "500002.SH", "500003.SH"])

            self.stock_list.clear()
            cmd = Command(Parameters(['fetch', 'SZ']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.stock_list, ["500004.SZ", "500005.SZ", "500006.SZ"])

    def test_fetch(self):
        self.stock_list = list()
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'get_stock_list_of_exchange', new = self.get_stock_list_of_exchange_mock):

            cmd = Command(Parameters(['fetch']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.stock_list, ["500001.SH", "500002.SH", "500003.SH", "500004.SZ", "500005.SZ", "500006.SZ"])

