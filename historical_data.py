"""
miesiecznie - 1 dnia kazdego miesiaca - jkis if z funkcja na koncu
miesiecznie takze dla brakow
dzienne = codziennie na zakonczenie dnia
dziennine - takze dla brakow

warunek wejscia - download_daily/monthly from files

dodatkowo warto zbudowac macierz, ktora pokaze braki, jesli sa

"""

# libs
import requests
import mysql.connector  # https://dev.mysql.com/doc/connector-python/en/
import json
from datetime import datetime, timedelta
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



DAILY_HISTORY_DAYS = 3

market = 'BTCUSDT'
tick_interval = '1m'
stock_type = 'spot'
stock_exchange = 'Binance.com'



# todo: filenames to download # daily first in dev. Max Last 62 days
def get_filenames_to_download():
    # todo: if is records get last + 1, else get all historical from last 62 days. GET ALSO MISSING DAYS <MAYBE OTHER FUNCTION WILL BE BETTER TO DO THIS????
    start_date = datetime.strptime(str(datetime.now() - timedelta(days=62))[0:10], "%Y-%m-%d")
    end_date = datetime.strptime(str(datetime.now() - timedelta(days=0))[0:10], "%Y-%m-%d")
    delta = end_date - start_date
    l = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        l.insert(i, str(day)[0:10])
        # print(day)
    return (l)

print(get_filenames_to_download())

sssss = get_filenames_to_download()[0]

print(sssss)


#https://data.binance.vision/?prefix=data/spot/daily/klines/BTCUSDT/

FILE_LENGTH = 'daily'
TYPE = 'klines'
APP_PATH = "tmp/"
FILENAME = "" + market +"-"+ tick_interval +"-"+ sssss +""
FILE_PATH = APP_PATH + FILENAME
BASE_URL = "https://data.binance.vision/data/"+stock_type+"/"+FILE_LENGTH+"/"+TYPE+"/"+market+"/"+tick_interval+"/"+FILENAME+".zip"

print(FILE_PATH)


# todo: file import
r = requests.get(BASE_URL)
open("tmp/" + market +"-"+ tick_interval +"-"+ sssss +".zip", "wb").write(r.content)

# todo: zip unpack
with zipfile.ZipFile("tmp/" + market +"-"+ tick_interval +"-"+ sssss +".zip", "r") as zip_ref:
    zip_ref.extractall("tmp")

# insert file into DBMS
csv_data = csv.reader(open("tmp/" + market +"-"+ tick_interval +"-"+ sssss +".csv"))
open_time_min = min(csv_data)[0]

csv_data = csv.reader(open("tmp/" + market +"-"+ tick_interval +"-"+ sssss +".csv"))
open_time_max = max(csv_data)[0]

csv_data = csv.reader(open("tmp/" + market +"-"+ tick_interval +"-"+ sssss +".csv"))
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