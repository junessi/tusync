import re
from common.constants import EXCHANGES, STOCK_CODE_ENDINGS

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

def get_stock_code_ending(ex):
    if ex in EXCHANGES:
        return STOCK_CODE_ENDINGS[ex]

    return ''