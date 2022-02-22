DECADES = [
    {'start': 19900101, 'end': 19991231, 'years': [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999]},
    {'start': 20000101, 'end': 20091231, 'years': [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009]},
    {'start': 20100101, 'end': 20191231, 'years': [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019]},
    {'start': 20200101, 'end': 20291231, 'years': [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029]}
]

EXCHANGES = [
    'SSE', # 上交所
    'SZSE' # 深交所
]

STOCK_CODE_SUBFIX = ['SH', 'SZ']

MAP_STOCK_CODE_SUBFIX_TO_EXCHANGE = {
    'SH': 'SSE',
    'SZ': 'SZSE'
}

MAP_EXCHANGE_TO_STOCK_CODE_SUBFIX = {
    'SSE': 'SH',
    'SZSE': 'SZ'
}
