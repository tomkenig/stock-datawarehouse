# libs
import requests
from datetime import datetime, timedelta
import datetime
import zipfile
import csv
from db_works import db_connect, db_tables
import queue_works

db_schema_name, db_table_name, db_settings_table_name = db_tables()
cursor, cnxn = db_connect()
TYPE = 'klines'
APP_PATH = "tmp/"

download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, range_to_download, download_api_interval_sec, daily_update_from_files, monthly_update_from_files, start_hist_download_ux_timestamp = queue_works.get_settings("monthly_hist")

# todo: function get single setting to download: curr, daily, monthly



def get_filenames_to_download_monthly():
    # todo: if is records get last + 1, else get all historical from last 62 days. GET ALSO MISSING DAYS <MAYBE OTHER FUNCTION WILL BE BETTER TO DO THIS????
    monthly_hist_days = int(datetime.datetime.utcnow().timestamp()) / 86400 - start_hist_download_ux_timestamp / 86400
    start_date = datetime.datetime.strptime(str(datetime.datetime.utcnow() - timedelta(days=monthly_hist_days))[0:10], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(str(datetime.datetime.utcnow() - timedelta(days=0))[0:10], "%Y-%m-%d")
    delta = end_date - start_date
    l = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        l.insert(i, "" + market +"-"+ tick_interval +"-"+ str(day)[0:7] +"")
        # print(day)
    return sorted(list(set(l))) # works like distinct

print(get_filenames_to_download_monthly())


def get_monthly_files():
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
        "DELETE FROM " + db_schema_name + "." + db_table_name + " where open_time >= %s and open_time <= %s and tick_interval = %s and data_granulation = %s and market = %s and stock_type = %s and stock_exchange = %s",
        (open_time_min, open_time_max, tick_interval, data_granulation, market, stock_type, stock_exchange))
    print("delete done")

    # insert data
    for i in csv_data:
        cursor.execute("INSERT INTO " + db_schema_name+"."+db_table_name +"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, `ignore`, market, tick_interval, stock_type, stock_exchange) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], market, tick_interval, stock_type, stock_exchange))
        print(i)

    print("insert done")



# todo: repair current month error
FILENAME_LIST_MONTHLY = get_filenames_to_download_monthly()
# monthly
for k in FILENAME_LIST_MONTHLY:
    try:
        FILENAME = k
        FILE_PATH = APP_PATH + FILENAME
        BASE_URL = "https://data.binance.vision/data/"+stock_type+"/monthly/"+TYPE+"/"+market+"/"+tick_interval+"/"+FILENAME+".zip"
        get_monthly_files()
        cnxn.commit()
    except:
        print(FILENAME + " probably not exist - generates error message")




cnxn.commit()
cursor.close()
cnxn.close()
# todo : there is a problem: on 0.15 ther in no new file daily in the list ['BTCUSDT-1m-2021-09-24', 'BTCUSDT-1m-2021-09-25', 'BTCUSDT-1m-2021-09-26']. MYBE THIS IS CORRECT