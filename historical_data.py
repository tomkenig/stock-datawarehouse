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

do matrix with gaps

MONTHLY DATA FIRST THAN DAILY -
add rollbacks and commits
"""

# libs
import requests
from datetime import datetime, timedelta
import datetime
import math
import zipfile
import csv
from db_works import db_connect, db_tables
# import queue_works


db_schema_name, db_table_name, db_settings_table_name = db_tables()
cursor, cnxn = db_connect()
TYPE = 'klines'
APP_PATH = "tmp/"

def get_settings_hist():
    cursor.execute("SELECT download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, "
                   "current_range_to_overwrite, download_api_interval_sec, daily_update_from_files, monthly_update_from_files "
                   "FROM " + db_schema_name + "." + db_settings_table_name + " WHERE daily_update_from_files = 1 and "
                                                                             "coalesce(next_download_ux_timestamp, 0) <= "
                   + str(int(datetime.datetime.utcnow().timestamp())) + " order by start_download_ux_timestamp asc limit 1")
    download_setting = cursor.fetchall()
    if len(download_setting) > 0:
         download_settings_id = download_setting[0][0]
         market = download_setting[0][1]
         tick_interval = download_setting[0][2]
         data_granulation = download_setting[0][3]
         stock_type = download_setting[0][4]
         stock_exchange = download_setting[0][5]
         range_to_download = download_setting[0][6]
         download_api_interval_sec = download_setting[0][7]
         daily_update_from_files = download_setting[0][8]
         monthly_update_from_files = download_setting[0][9]
    else:
         print("no data to download")
         exit()

    # block current setting changing its status
    cursor.execute("UPDATE " + db_schema_name + "." + db_settings_table_name + " SET download_setting_status_id = %s where download_settings_id = %s", (1, download_settings_id))
    cnxn.commit()
    print("settings blocked")
    return download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, range_to_download, download_api_interval_sec, daily_update_from_files, monthly_update_from_files


download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, range_to_download, download_api_interval_sec, daily_update_from_files, monthly_update_from_files, start_hist_download_ux_timestamp = get_settings("monthly_hist")

# todo: function get single setting to download: curr, daily, monthly

DAILY_HISTORY_DAYS = 3
MONTHLY_HISTORY_DAYS = 30

# todo: filenames to download # daily first in dev. Max Last 62 days
def get_filenames_to_download_daily():
    # todo: if is records get last + 1, else get all historical from last 62 days. GET ALSO MISSING DAYS <MAYBE OTHER FUNCTION WILL BE BETTER TO DO THIS????
    start_date = datetime.datetime.strptime(str(datetime.datetime.utcnow() - timedelta(days=DAILY_HISTORY_DAYS))[0:10], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(str(datetime.datetime.utcnow() - timedelta(days=1))[0:10], "%Y-%m-%d")
    delta = end_date - start_date
    l = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        l.insert(i, "" + market +"-"+ tick_interval +"-"+ str(day)[0:10] +"")
        # print(day)
    return sorted(l)


def get_filenames_to_download_monthly():
    # todo: if is records get last + 1, else get all historical from last 62 days. GET ALSO MISSING DAYS <MAYBE OTHER FUNCTION WILL BE BETTER TO DO THIS????
    start_date = datetime.datetime.strptime(str(datetime.datetime.utcnow() - timedelta(days=MONTHLY_HISTORY_DAYS))[0:10], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(str(datetime.datetime.utcnow() - timedelta(days=0))[0:10], "%Y-%m-%d")
    delta = end_date - start_date
    l = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        l.insert(i, "" + market +"-"+ tick_interval +"-"+ str(day)[0:7] +"")
        # print(day)
    return sorted(list(set(l))) # works like distinct



print(get_filenames_to_download_daily())
print(get_filenames_to_download_monthly())




def get_daily_files():
    # todo: file import
    r = requests.get(BASE_URL)
    open(FILE_PATH + ".zip", "wb").write(r.content)

    # todo: zip unpack
    with zipfile.ZipFile(FILE_PATH + ".zip", "r") as zip_ref:
        zip_ref.extractall("tmp")

    # get data from csv file
    with open(FILE_PATH + ".csv") as file_handle:
        csv_reader = csv.reader(file_handle)
        csv_data = [row for row in csv_reader]

    open_time_min = min(csv_data)[0]
    open_time_max = max(csv_data)[0]


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