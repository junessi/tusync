import re
from common.constants import EXCHANGES, MAP_EXCHANGE_TO_STOCK_CODE_SUBFIX, MAP_STOCK_CODE_SUBFIX_TO_EXCHANGE, STOCK_CODE_SUBFIX

def is_year(s):
    return re.search(r'[12][09][0-9]{2}', s) != None

def is_date(s):
    return re.search(r'[0-9]{8}', s) != None

def is_stock_code(s):
    return re.search(r'[0-9]{6}\.(SH|SZ)', s) != None

def is_negative_number(s):
    return re.search(r'-[0-9]+$', s) != None

def is_exchange(ex):
    return ex in EXCHANGES

def get_exchange(subfix):
    return MAP_STOCK_CODE_SUBFIX_TO_EXCHANGE[subfix] if subfix in STOCK_CODE_SUBFIX else ''

def is_stock_code_subfix(ex):
    return ex in STOCK_CODE_SUBFIX

def get_stock_code_subfix(ex):
    return MAP_EXCHANGE_TO_STOCK_CODE_SUBFIX[ex] if ex in EXCHANGES else ''

def get_first_date_of_year(y):
    return int(y) * 10000 + 101

def get_last_date_of_year(y):
    return int(y) * 10000 + 1231
