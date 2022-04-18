# tusync
A tool for fetching and storing tushare data to local database.

## Credentials
Create or edit ~/.tusync_credentials to have the following content:
```
token=<tushare token>
mysql_server=<server ip>
mysql_db=<db name>
mysql_user=<db user>
mysql_password=<db password>
mysql_charset=<db charset>   # for example: utf8mb4
```

## Supported exchanges

| exchange | code |
| ------------- | ------------- |
| Shanghai Stock Exchange | SH |
| Shenzhen Stock Exchange | SZ |

## Commands
### fetch
fetch latest stock list of an exchange:
```
tusync fetch SZ # fetch latest stock list of Shenzhen Stock Exchange
```

### update
update today's stocks in all exchanges(same as "update today"):
```
tusync update
# or
tusync update today
```

update all stocks in all exchanges in the whole history:
```
tusync update full
```

update all stocks in all exchanges in the last N days, counted from today, closed days will also be counted.
```
tusync update -1 # same as "tusync update today"
tusync update -2 # will update today and yesterday
tusync update -3 # will update today, yesterday and the day before yesterday
tusync update -100 # will update today, yesterday, the day before yesterday and other 97 days.
```

update all stocks in all exchanges in a date range:
```
tusync update 20210801 20220122 # update all stocks in all exchanges from 20210801 to 20220122
```

update a stock from the last updated date
```
tusync update 123456.SH # update stock 123456 in Shanghai Stock Exchange from last updated date
                        # if there is no last updated date the whole history of this stock will be updated.
```

update a stock in a specified year:
```
tusync update 123456.SH 2021 # update stock 123456 in Shanghai Stock Exchange from 20210101 to 20211231
```

update a stock from a specifed date:
```
tusync update 123456.SZ 20210321 # update stock 123456 in Shenzhen Stock Exchange from 20210321 to today
```

update a stock in a date range:
```
tusync update 123456.SZ 20210701 20220621 # update stock 123456 in Shenzhen Stock Exchange from 20210701 to 20220621
```

update all stocks in an exchange from a specified date:
```
tusync update SH 20210801 # update all stocks in Shanghai Stock Exchange from 20210801 to today
```

update all stocks in an exchange in a date range:
```
tusync update SH 20210801 20220122 # update all stocks in Shanghai Stock Exchange from 20210801 to 20220122
```

