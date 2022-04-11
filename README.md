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

## Commands
### fetch
```
tusync fetch [exchange]
```
For example, the following command will fetch the latest stock list of Shanghai Exchange:
```
tusync fetch SH
```

### update
update all stocks in all exchanges:
```
tusync update
```






