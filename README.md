# stock-datawarehouse
Finance OHLC Data Warehouse for Cryptocurencies listen on Binance and other stock markets
Application downloads market data in defined time intervals and upload it to database

# Versions
Version 0.01 MVP:
In the first steps and app MVP version download binance BTCUSDT data and upload it to MySQL database.
Application is stable and can works on production env.
Application or view on database transforms OHLC data
Market data are downloaded and can by start by crontab or other Task Manager
Application use historical data and API data to get current OHLC values

# Data
Binance klines data
Fear and greed index

# Future:
Data repair processes are implemented. In case of situatuation, when there is no data to download or connection are temporary broken / lost
There is also repair process witch downloads daily data once a day that overwrite data
There is also repair process witch downloads monthly data once a month that overwrite data
Transactions used in database DML
App can download data from other stock exchanges (not only Binance) and other markets (ForEx also)
monitoring, error logs, checksums
App calculates how many periond are needed to download (current number of periods is fixed in settings)
supports other databases technology (MSSQL, PgSQL, Oracle, SQL Lite etc.)
supports NoSQL env (S3&Athena, JSON DBs like MongoDB or DynamoDB)

# Database Objects
Object names:
binance_download_settings
binance_klines_data
vw_binance_klines_anl

# Short Install & Deployment
ENV
mkdir /usr/home/[LOGIN]/.virtualenvs 
cd /usr/home/[LOGIN]/.virtualenvs
virtualenv [ENV_NAME] -p /usr/local/bin/python3.9 
source /usr/home/ [LOGIN] /.virtualenvs/ [ENV_NAME] /bin/activate 
pip install requests
pip install  mysql-connector-python
