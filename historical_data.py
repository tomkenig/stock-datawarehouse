# libs
import requests
import mysql.connector  # https://dev.mysql.com/doc/connector-python/en/
import json
import datetime
import math
import zipfile
import csv

# get database connection credentials from JSON file
with open('db_credentials.json') as json_conf:
    sql_db_conn = (json.load(json_conf))

# db driver (MySQL) connection settings
cnxn = mysql.connector.connect(user=sql_db_conn["user"],
                               password=sql_db_conn["password"],
                               host=sql_db_conn["host"],
                               database=sql_db_conn["database"])

# destination
db_schema_name = sql_db_conn["db_schema_name"]  # schema_name
db_table_name = sql_db_conn["db_table_name"]  # table_name
db_settings_table_name = sql_db_conn["db_settings_table_name"]  # settings table name

# open db connection
cursor = cnxn.cursor()

#https://data.binance.vision/?prefix=data/spot/daily/klines/BTCUSDT/
BASE_URL = 'https://data.binance.vision/data/spot/daily/klines/BTCUSDT/1m/BTCUSDT-1m-2021-03-17.zip'
FILE_LENGTH = 'daily'
TYPE = 'klines'

ts = str(math.floor(datetime.datetime.now().timestamp()))

market = 'BTCUSDT'
tick_interval = '1m'
stock_type = 'spot'
stock_exchange = 'Binance.com'

# todo: file import
r = requests.get(BASE_URL)
open('tmp/BTCUSDT-1m-2017-03-17.zip', 'wb').write(r.content)

# todo: zip unpack
with zipfile.ZipFile("tmp/BTCUSDT-1m-2017-03-17.zip", "r") as zip_ref:
    zip_ref.extractall("tmp")

# insert file into DBMS
csv_data = csv.reader(open('tmp/BTCUSDT-1m-2017-03-17.csv'))
open_time_min = min(csv_data)[0]

csv_data = csv.reader(open('tmp/BTCUSDT-1m-2017-03-17.csv'))
open_time_max = max(csv_data)[0]

csv_data = csv.reader(open('tmp/BTCUSDT-1m-2017-03-17.csv'))
# delete old data to overwrite
cursor.execute(
    "DELETE FROM " + db_schema_name + "." + db_table_name + " where open_time >= %s and open_time <= %s and tick_interval = %s and market = %s and stock_type = %s and stock_exchange = %s",
    (open_time_min, open_time_max, tick_interval, market, stock_type, stock_exchange))
print("delete done")

# insert data
for i in csv_data:
    cursor.execute("INSERT INTO " + db_schema_name+"."+db_table_name +"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, `ignore`, market, tick_interval, stock_type, stock_exchange) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], market, tick_interval, stock_type, stock_exchange))
    print(i)
cnxn.commit()
cursor.close()
cnxn.close()
print("insert done")