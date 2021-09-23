# stock-datawarehouse
 Finance OHLC Data Warehouse for Binance Cryptocurencies
Application downloads market data in serveral time intervals and upload it to database

# Versions
Version 0.05a MVP:

In the first steps and app MVP version download binance BTCUSDT data and upload it to MySQL database.
Application is stable and works on production env.

# Future:

Application or view on database transforms OHLC data
Market data are downloaded once a hour and uses crontab
Data repair processes are implemented. In case of situatuation, when there is no data to download or connection are temporary broken / lost
Application use historical data and API data to get current OHLC values
In the next steps app will download other interwals provided in JSON file or in database
There is also repair process witch downloads daily data once a day that overwrite data
There is also repair process witch downloads monthly data once a month that overwrite data
Transactions in database DML
App can download data from other markets
monitoring, error logs, checksums
App calculates how many periond are needed to download (current number of periods is fixed in settings)
supports other databases technology (MSSQL, PgSQL, Oracle, SQL Lite etc.)

# Database Objects
Object names
Details tables:

klines_binance
Dimensions:

download_settings
Short Install & Deployment
ENV
mkdir /usr/home/[LOGIN]/.virtualenvs 
cd /usr/home/[LOGIN]/.virtualenvs
virtualenv [ENV_NAME] -p /usr/local/bin/python3.9 
source /usr/home/ [LOGIN] /.virtualenvs/ [ENV_NAME] /bin/activate 
pip install requests
pip install  mysql-connector-python