from datetime import datetime
import unittest

from command.Update import Update
from command.Command import Command
from command.State import State
from command.Parameters import Parameters
from data.TUData import TUData
from data.local.Database import Database
from unittest.mock import patch

class testUpdate(unittest.TestCase):
    def setUp(self):
        self.updated_stock_codes = list()

    def init_TUData(self):
        pass

    def update_daily_mock(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        self.updated_stock_codes.append("{0}.{1}".format(stock_code, exchange))

    def get_stock_list_mock(self, exchange):
        data = type('', (object, ), {'ts_code': list()})() # anonymous object
        if exchange == "SSE":
            data.ts_code = ["100001.SH", "100002.SH", "100003.SH"]
        elif exchange == "SZSE":
            data.ts_code = ["200001.SZ", "200002.SZ", "200003.SZ"]

        return data

    def test_update(self):
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'update_daily', new = self.update_daily_mock), \
             patch.object(TUData, 'get_stock_list', new = self.get_stock_list_mock):
            cmd = Command(Parameters(['update']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stock_codes, ['100001.SSE', '100002.SSE', '100003.SSE',
                                                        '200001.SZSE', '200002.SZSE', '200003.SZSE'])


class testUpdateFull(unittest.TestCase):
    def init_TUData(self):
        pass

    def update_daily_mock(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        self.updated_stocks.append(["{0}.{1}".format(stock_code, exchange), start_date, end_date])

    def get_stock_list_mock(self, exchange):
        data = type('', (object, ), {'ts_code': list()})() # anonymous object
        if exchange == "SSE":
            data.ts_code = ["100001.SH"]
        elif exchange == "SZSE":
            data.ts_code = ["200001.SZ"]

        return data

    def test_update_full(self):
        self.updated_stocks = list(list())
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'update_daily', new = self.update_daily_mock), \
             patch.object(TUData, 'get_stock_list', new = self.get_stock_list_mock):
            cmd = Command(Parameters(['update', 'full']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks[0],  ['100001.SSE', '19900101', '19901231'])
            self.assertEqual(self.updated_stocks[1],  ['200001.SZSE', '19900101', '19901231'])
            self.assertEqual(self.updated_stocks[2],  ['100001.SSE', '19910101', '19911231'])
            self.assertEqual(self.updated_stocks[3],  ['200001.SZSE', '19910101', '19911231'])
            self.assertEqual(self.updated_stocks[4],  ['100001.SSE', '19920101', '19921231'])
            self.assertEqual(self.updated_stocks[5],  ['200001.SZSE', '19920101', '19921231'])
            self.assertEqual(self.updated_stocks[6],  ['100001.SSE', '19930101', '19931231'])
            self.assertEqual(self.updated_stocks[7],  ['200001.SZSE', '19930101', '19931231'])
            self.assertEqual(self.updated_stocks[8],  ['100001.SSE', '19940101', '19941231'])
            self.assertEqual(self.updated_stocks[9],  ['200001.SZSE', '19940101', '19941231'])
            self.assertEqual(self.updated_stocks[10], ['100001.SSE', '19950101', '19951231'])
            self.assertEqual(self.updated_stocks[11], ['200001.SZSE', '19950101', '19951231'])
            self.assertEqual(self.updated_stocks[12], ['100001.SSE', '19960101', '19961231'])
            self.assertEqual(self.updated_stocks[13], ['200001.SZSE', '19960101', '19961231'])
            self.assertEqual(self.updated_stocks[14], ['100001.SSE', '19970101', '19971231'])
            self.assertEqual(self.updated_stocks[15], ['200001.SZSE', '19970101', '19971231'])
            self.assertEqual(self.updated_stocks[16], ['100001.SSE', '19980101', '19981231'])
            self.assertEqual(self.updated_stocks[17], ['200001.SZSE', '19980101', '19981231'])
            self.assertEqual(self.updated_stocks[18], ['100001.SSE', '19990101', '19991231'])
            self.assertEqual(self.updated_stocks[19], ['200001.SZSE', '19990101', '19991231'])
            self.assertEqual(self.updated_stocks[20], ['100001.SSE', '20000101', '20001231'])
            self.assertEqual(self.updated_stocks[21], ['200001.SZSE', '20000101', '20001231'])
            self.assertEqual(self.updated_stocks[22], ['100001.SSE', '20010101', '20011231'])
            self.assertEqual(self.updated_stocks[23], ['200001.SZSE', '20010101', '20011231'])
            self.assertEqual(self.updated_stocks[24], ['100001.SSE', '20020101', '20021231'])
            self.assertEqual(self.updated_stocks[25], ['200001.SZSE', '20020101', '20021231'])
            self.assertEqual(self.updated_stocks[26], ['100001.SSE', '20030101', '20031231'])
            self.assertEqual(self.updated_stocks[27], ['200001.SZSE', '20030101', '20031231'])
            self.assertEqual(self.updated_stocks[28], ['100001.SSE', '20040101', '20041231'])
            self.assertEqual(self.updated_stocks[29], ['200001.SZSE', '20040101', '20041231'])
            self.assertEqual(self.updated_stocks[30], ['100001.SSE', '20050101', '20051231'])
            self.assertEqual(self.updated_stocks[31], ['200001.SZSE', '20050101', '20051231'])
            self.assertEqual(self.updated_stocks[32], ['100001.SSE', '20060101', '20061231'])
            self.assertEqual(self.updated_stocks[33], ['200001.SZSE', '20060101', '20061231'])
            self.assertEqual(self.updated_stocks[34], ['100001.SSE', '20070101', '20071231'])
            self.assertEqual(self.updated_stocks[35], ['200001.SZSE', '20070101', '20071231'])
            self.assertEqual(self.updated_stocks[36], ['100001.SSE', '20080101', '20081231'])
            self.assertEqual(self.updated_stocks[37], ['200001.SZSE', '20080101', '20081231'])
            self.assertEqual(self.updated_stocks[38], ['100001.SSE', '20090101', '20091231'])
            self.assertEqual(self.updated_stocks[39], ['200001.SZSE', '20090101', '20091231'])
            self.assertEqual(self.updated_stocks[40], ['100001.SSE', '20100101', '20101231'])
            self.assertEqual(self.updated_stocks[41], ['200001.SZSE', '20100101', '20101231'])
            self.assertEqual(self.updated_stocks[42], ['100001.SSE', '20110101', '20111231'])
            self.assertEqual(self.updated_stocks[43], ['200001.SZSE', '20110101', '20111231'])
            self.assertEqual(self.updated_stocks[44], ['100001.SSE', '20120101', '20121231'])
            self.assertEqual(self.updated_stocks[45], ['200001.SZSE', '20120101', '20121231'])
            self.assertEqual(self.updated_stocks[46], ['100001.SSE', '20130101', '20131231'])
            self.assertEqual(self.updated_stocks[47], ['200001.SZSE', '20130101', '20131231'])
            self.assertEqual(self.updated_stocks[48], ['100001.SSE', '20140101', '20141231'])
            self.assertEqual(self.updated_stocks[49], ['200001.SZSE', '20140101', '20141231'])
            self.assertEqual(self.updated_stocks[50], ['100001.SSE', '20150101', '20151231'])
            self.assertEqual(self.updated_stocks[51], ['200001.SZSE', '20150101', '20151231'])
            self.assertEqual(self.updated_stocks[52], ['100001.SSE', '20160101', '20161231'])
            self.assertEqual(self.updated_stocks[53], ['200001.SZSE', '20160101', '20161231'])
            self.assertEqual(self.updated_stocks[54], ['100001.SSE', '20170101', '20171231'])
            self.assertEqual(self.updated_stocks[55], ['200001.SZSE', '20170101', '20171231'])
            self.assertEqual(self.updated_stocks[56], ['100001.SSE', '20180101', '20181231'])
            self.assertEqual(self.updated_stocks[57], ['200001.SZSE', '20180101', '20181231'])
            self.assertEqual(self.updated_stocks[58], ['100001.SSE', '20190101', '20191231'])
            self.assertEqual(self.updated_stocks[59], ['200001.SZSE', '20190101', '20191231'])
            self.assertEqual(self.updated_stocks[60], ['100001.SSE', '20200101', '20201231'])
            self.assertEqual(self.updated_stocks[61], ['200001.SZSE', '20200101', '20201231'])
            self.assertEqual(self.updated_stocks[62], ['100001.SSE', '20210101', '20211231'])
            self.assertEqual(self.updated_stocks[63], ['200001.SZSE', '20210101', '20211231'])

            today = int(datetime.today().strftime("%Y%m%d"))
            start_date = "{0}".format(today - (today%10000) + 101) # form YYYY0101
            end_date = "{0}".format(today)
            self.assertEqual(self.updated_stocks[-1][0], '200001.SZSE')
            self.assertEqual(self.updated_stocks[-1][1], start_date)
            self.assertEqual(self.updated_stocks[-1][2], end_date)


class testUpdateLastNDays(unittest.TestCase):
    def init_TUData(self):
        pass

    def update_last_n_days_mock(self, n):
        self.last_n = n
        return State.DONE

    def test_update_last_n_days(self):
        self.last_n = 0
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(Update, 'update_last_n_days', new = self.update_last_n_days_mock):
            cmd = Command(Parameters(['update', 'today']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.last_n, 1)

            cmd = Command(Parameters(['update', '-1']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.last_n, 1)

            cmd = Command(Parameters(['update', '-2']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.last_n, 2)

            cmd = Command(Parameters(['update', '-5']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.last_n, 5)

            cmd = Command(Parameters(['update', '-10000']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.last_n, 10000)

class testUpdateStockCode(unittest.TestCase):
    def setUp(self):
        self.updated_stocks = list(list())

    def init_TUData(self):
        pass

    def init_Database(self):
        pass

    def update_daily_mock(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        self.updated_stocks.append(["{0}.{1}".format(stock_code, exchange), start_date, end_date])

    def get_last_updated_date_mock(self, exchange, stock_code):
        return 20200101

    def test_update_stock_code(self):
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'update_daily', new = self.update_daily_mock), \
             patch.object(Database, '__init__', new = self.init_Database), \
             patch.object(Database, 'get_last_updated_date', new = self.get_last_updated_date_mock):
            cmd = Command(Parameters(['update', '600699.SZ']))
            self.assertEqual(cmd.get_state(), State.DONE)
            today = "{}".format(datetime.today().strftime("%Y%m%d"))
            self.assertEqual(self.updated_stocks, [['600699.SZ', '20200102', today]])


class testUpdateStockCodeYear(unittest.TestCase):
    def setUp(self):
        self.updated_stocks = list(list())

    def init_TUData(self):
        pass

    def update_daily_mock(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        self.updated_stocks.append(["{0}.{1}".format(stock_code, exchange), start_date, end_date])

    def test_update_stock_code(self):
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'update_daily', new = self.update_daily_mock):
            cmd = Command(Parameters(['update', '600699.SZ', '2011']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks, [['600699.SZ', '20110101', '20111231']])


class testUpdateStockCodeFromDate(unittest.TestCase):
    def init_TUData(self):
        pass

    def update_daily_mock(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        self.updated_stocks.append(["{0}.{1}".format(stock_code, exchange), start_date, end_date])

    def test_update_stock_code_from_date(self):
        self.updated_stocks = list(list())
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'update_daily', new = self.update_daily_mock):
            cmd = Command(Parameters(['update', '600688.SZ', '20200621']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks, [['600688.SZ', '20200621', '']])


class testUpdateStockCodeFromToDate(unittest.TestCase):
    def setUp(self):
        self.updated_stocks = list(list())

    def init_TUData(self):
        pass

    def update_daily_mock(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        self.updated_stocks.append(["{0}.{1}".format(stock_code, exchange), start_date, end_date])

    def test_update_stock_code_from_to_date(self):
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'update_daily', new = self.update_daily_mock):
            cmd = Command(Parameters(['update', '600688.SZ', '20200621', '20200920']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks, [['600688.SZ', '20200621', '20200920']])

            self.updated_stocks.clear()
            cmd = Command(Parameters(['update', '600688.SZ', '20200621', '20220920']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks, [['600688.SZ', '20200621', '20220920']])


class testUpdateExchangeFromDate(unittest.TestCase):
    def setUp(self):
        self.updated_stocks = list(list())

    def init_TUData(self):
        pass

    def update_daily_mock(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        self.updated_stocks.append(["{0}.{1}".format(stock_code, exchange), start_date, end_date])

    def get_stock_list_mock(self, exchange):
        data = type('', (object, ), {'ts_code': list()})() # anonymous object
        if exchange == "SSE":
            data.ts_code = ["300001.SH", "300002.SH", "300003.SH"]
        elif exchange == "SZSE":
            data.ts_code = ["300004.SZ", "300005.SZ", "300006.SZ"]

        return data

    def test_update_exchange_from_date(self):
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'update_daily', new = self.update_daily_mock), \
             patch.object(TUData, 'get_stock_list', new = self.get_stock_list_mock):

            cmd = Command(Parameters(['update', 'SH', '20200301']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks, [['300001.SH', '20200301', ''], ['300002.SH', '20200301', ''], ['300003.SH', '20200301', '']])

            self.updated_stocks.clear()
            cmd = Command(Parameters(['update', 'SZ', '20200301']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks, [['300004.SZ', '20200301', ''], ['300005.SZ', '20200301', ''], ['300006.SZ', '20200301', '']])


class testUpdateExchangeFromToDate(unittest.TestCase):
    def setUp(self):
        self.updated_stocks = list(list())

    def init_TUData(self):
        pass

    def update_daily_mock(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        self.updated_stocks.append(["{0}.{1}".format(stock_code, exchange), start_date, end_date])

    def get_stock_list_mock(self, exchange):
        data = type('', (object, ), {'ts_code': list()})() # anonymous object
        if exchange == "SSE":
            data.ts_code = ["300001.SH", "300002.SH", "300003.SH"]
        elif exchange == "SZSE":
            data.ts_code = ["300004.SZ", "300005.SZ", "300006.SZ"]

        return data

    def test_update_exchange_from_date(self):
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'update_daily', new = self.update_daily_mock), \
             patch.object(TUData, 'get_stock_list', new = self.get_stock_list_mock):

            cmd = Command(Parameters(['update', 'SH', '20200301', '20221130']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks, [['300001.SH', '20200301', '20221130'],
                                                   ['300002.SH', '20200301', '20221130'],
                                                   ['300003.SH', '20200301', '20221130']])

            self.updated_stocks.clear()
            cmd = Command(Parameters(['update', 'SZ', '20200301', '20221031']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks, [['300004.SZ', '20200301', '20221031'],
                                                   ['300005.SZ', '20200301', '20221031'],
                                                   ['300006.SZ', '20200301', '20221031']])


class testUpdateFromDate(unittest.TestCase):
    def setUp(self):
        self.updated_stocks = list(list())

    def init_TUData(self):
        pass

    def update_daily_mock(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        self.updated_stocks.append(["{0}.{1}".format(stock_code, exchange), start_date, end_date])

    def get_stock_list_mock(self, exchange):
        data = type('', (object, ), {'ts_code': list()})() # anonymous object
        if exchange == "SSE":
            data.ts_code = ["400001.SH", "400002.SH", "400003.SH"]
        elif exchange == "SZSE":
            data.ts_code = ["400004.SZ", "400005.SZ", "400006.SZ"]

        return data

    def test_update_exchange_from_date(self):
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'update_daily', new = self.update_daily_mock), \
             patch.object(TUData, 'get_stock_list', new = self.get_stock_list_mock):

            cmd = Command(Parameters(['update', '20200201']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks, [['400001.SH', '20200201', ''],
                                                   ['400002.SH', '20200201', ''],
                                                   ['400003.SH', '20200201', ''],
                                                   ['400004.SZ', '20200201', ''],
                                                   ['400005.SZ', '20200201', ''],
                                                   ['400006.SZ', '20200201', '']])

class testUpdateFromToDate(unittest.TestCase):
    def setUp(self):
        self.updated_stocks = list(list())

    def init_TUData(self):
        pass

    def update_daily_mock(self, exchange, stock_code, trade_date = '', start_date = '', end_date = ''):
        self.updated_stocks.append(["{0}.{1}".format(stock_code, exchange), start_date, end_date])

    def get_stock_list_mock(self, exchange):
        data = type('', (object, ), {'ts_code': list()})() # anonymous object
        if exchange == "SSE":
            data.ts_code = ["400001.SH", "400002.SH", "400003.SH"]
        elif exchange == "SZSE":
            data.ts_code = ["400004.SZ", "400005.SZ", "400006.SZ"]

        return data

    def test_update_exchange_from_date(self):
        with patch.object(TUData, '__init__', new = self.init_TUData), \
             patch.object(TUData, 'update_daily', new = self.update_daily_mock), \
             patch.object(TUData, 'get_stock_list', new = self.get_stock_list_mock):

            cmd = Command(Parameters(['update', '20200201', '20221031']))
            self.assertEqual(cmd.get_state(), State.DONE)
            self.assertEqual(self.updated_stocks, [['400001.SH', '20200201', '20221031'],
                                                   ['400002.SH', '20200201', '20221031'],
                                                   ['400003.SH', '20200201', '20221031'],
                                                   ['400004.SZ', '20200201', '20221031'],
                                                   ['400005.SZ', '20200201', '20221031'],
                                                   ['400006.SZ', '20200201', '20221031']])


