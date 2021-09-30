"""
FLOW:
1. Import all lib that are needed
2. Get DB credentials
3. Open DB connection
4. Monthly historicl data
4.1. start condition: If monthly_update_from_files = 1
4.1.1 download after date start_download_ux_timestamp if there are months to download before current
after download update monthly_hist_first_run = 1
after download update start_download_ux_timestamp to first day of month taht has been downloaded




miesiecznie - 1 dnia kazdego miesiaca - jkis if z funkcja na koncu
miesiecznie takze dla brakow
dzienne = codziennie na zakonczenie dnia
dziennine - takze dla brakow

warunek wejscia - download_daily/monthly from files

dodatkowo warto zbudowac macierz, ktora pokaze braki, jesli sa

MONTHLY DATA FIRST THAN DAILY -
add rollbacks and commits
"""

# libs
# import stockdwh_functions
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

cursor.execute("SELECT download_settings_id, market, tick_interval, stock_type, stock_exchange, api_range_to_overwrite, download_interval_sec, daily_update_from_files, monthly_update_from_files FROM " + db_schema_name + "." + db_settings_table_name + " WHERE daily_update_from_files = 1 and daily_hist_complete = 0 order by start_download_ux_timestamp asc limit 1")
download_setting = cursor.fetchall()
download_settings_id = download_setting[0][0]
market = download_setting[0][1]
tick_interval = download_setting[0][2]
stock_type = download_setting[0][3]
stock_exchange = download_setting[0][4]
range_to_download = download_setting[0][5]
download_interval_sec = download_setting[0][6]
daily_update_from_files = download_setting[0][7]
monthly_update_from_files = download_setting[0][8]

# todo: function get single setting to download: curr, daily, monthly

DAILY_HISTORY_DAYS = 3
MONTHLY_HISTORY_DAYS = 30

# todo: filenames to download # daily first in dev. Max Last 62 days
def get_filenames_to_download_daily():
    # todo: if is records get last + 1, else get all historical from last 62 days. GET ALSO MISSING DAYS <MAYBE OTHER FUNCTION WILL BE BETTER TO DO THIS????
    start_date = datetime.strptime(str(datetime.utcnow() - timedelta(days=DAILY_HISTORY_DAYS))[0:10], "%Y-%m-%d")
    end_date = datetime.strptime(str(datetime.utcnow() - timedelta(days=1))[0:10], "%Y-%m-%d")
    delta = end_date - start_date
    l = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        l.insert(i, "" + market +"-"+ tick_interval +"-"+ str(day)[0:10] +"")
        # print(day)
    return sorted(l)


def get_filenames_to_download_monthly():
    # todo: if is records get last + 1, else get all historical from last 62 days. GET ALSO MISSING DAYS <MAYBE OTHER FUNCTION WILL BE BETTER TO DO THIS????
    start_date = datetime.strptime(str(datetime.utcnow() - timedelta(days=MONTHLY_HISTORY_DAYS))[0:10], "%Y-%m-%d")
    end_date = datetime.strptime(str(datetime.utcnow() - timedelta(days=0))[0:10], "%Y-%m-%d")
    delta = end_date - start_date
    l = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        l.insert(i, "" + market +"-"+ tick_interval +"-"+ str(day)[0:7] +"")
        # print(day)
    return sorted(list(set(l))) # works like distinct



print(get_filenames_to_download_daily())
print(get_filenames_to_download_monthly())

TYPE = 'klines'
APP_PATH = "tmp/"


def get_daily_files():
    # todo: file import
    r = requests.get(BASE_URL)
    open(FILE_PATH + ".zip", "wb").write(r.content)

    # todo: zip unpack
    with zipfile.ZipFile(FILE_PATH + ".zip", "r") as zip_ref:
        zip_ref.extractall("tmp")

    # insert file into DBMS
    csv_data = csv.reader(open(FILE_PATH +".csv"))
    open_time_min = min(csv_data)[0]

    csv_data = csv.reader(open(FILE_PATH +".csv"))
    open_time_max = max(csv_data)[0]

    csv_data = csv.reader(open(FILE_PATH +".csv"))
    # delete old data to overwrite
    cursor.execute(
        "DELETE FROM " + db_schema_name + "." + db_table_name + " where open_time >= %s and open_time <= %s and tick_interval = %s and market = %s and stock_type = %s and stock_exchange = %s",
        (open_time_min, open_time_max, tick_interval, market, stock_type, stock_exchange))
    print("delete done")

    # insert data
    for i in csv_data:
        cursor.execute("INSERT INTO " + db_schema_name+"."+db_table_name +"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, `ignore`, market, tick_interval, stock_type, stock_exchange) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], market, tick_interval, stock_type, stock_exchange))
        print(i)

    print("insert done")



def get_monthly_files():
    # todo: file import
    r = requests.get(BASE_URL)
    open(FILE_PATH + ".zip", "wb").write(r.content)

    # todo: zip unpack
    with zipfile.ZipFile(FILE_PATH + ".zip", "r") as zip_ref:
        zip_ref.extractall("tmp")

    # insert file into DBMS
    csv_data = csv.reader(open(FILE_PATH +".csv"))
    open_time_min = min(csv_data)[0]

    csv_data = csv.reader(open(FILE_PATH +".csv"))
    open_time_max = max(csv_data)[0]

    csv_data = csv.reader(open(FILE_PATH +".csv"))
    # delete old data to overwrite
    cursor.execute(
        "DELETE FROM " + db_schema_name + "." + db_table_name + " where open_time >= %s and open_time <= %s and tick_interval = %s and market = %s and stock_type = %s and stock_exchange = %s",
        (open_time_min, open_time_max, tick_interval, market, stock_type, stock_exchange))
    print("delete done")

    # insert data
    for i in csv_data:
        cursor.execute("INSERT INTO " + db_schema_name+"."+db_table_name +"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, `ignore`, market, tick_interval, stock_type, stock_exchange) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], market, tick_interval, stock_type, stock_exchange))
        print(i)

    print("insert done")




def daily_hist_update():
    print("todo")

def monthly_hist_update():
    print("todo")


FILENAME_LIST_DAILY = get_filenames_to_download_daily()

# daily files

try:
    for j in FILENAME_LIST_DAILY:
        FILENAME = j
        FILE_PATH = APP_PATH + FILENAME
        BASE_URL = "https://data.binance.vision/data/"+stock_type+"/daily/"+TYPE+"/"+market+"/"+tick_interval+"/"+FILENAME+".zip"
        get_daily_files()
        cnxn.commit()
except:
     print("error_1")

# todo: repair current month error
FILENAME_LIST_MONTHLY = get_filenames_to_download_monthly()
# monthly
try:
    for k in FILENAME_LIST_MONTHLY:
        FILENAME = k
        FILE_PATH = APP_PATH + FILENAME
        BASE_URL = "https://data.binance.vision/data/"+stock_type+"/monthly/"+TYPE+"/"+market+"/"+tick_interval+"/"+FILENAME+".zip"
        get_monthly_files()
        cnxn.commit()
except:
    print("error_2")


cnxn.commit()
cursor.close()
cnxn.close()
# todo : there is a problem: on 0.15 ther in no new file daily in the list ['BTCUSDT-1m-2021-09-24', 'BTCUSDT-1m-2021-09-25', 'BTCUSDT-1m-2021-09-26']. MYBE THIS IS CORRECT