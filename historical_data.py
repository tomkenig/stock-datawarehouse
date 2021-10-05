# todo: check commits and rollbacks
# todo: get_filenames_to_download_monthly and get_filenames_to_download_daily can be one function
# todo: daily can start when monthly is completed
# todo: parallel start historical_data can have a problem - files deletion in one instance, when other instace works with files. Crash

# libs
import requests
from datetime import datetime, timedelta
import datetime
import zipfile
import csv
from db_works import db_connect, db_tables
import queue_works
import os

# path to downloaded files
TMP_PATH = "tmp/"

def delete_old_files():
    for f in os.listdir(TMP_PATH[0:len(TMP_PATH)-1]):
        os.remove(os.path.join(TMP_PATH[0:len(TMP_PATH)-1], f))
    print("old files deleted")


def get_filenames_to_download(interval_param_):
    # todo: if is records get last + 1, else get all historical from last 62 days. GET ALSO MISSING DAYS <MAYBE OTHER FUNCTION WILL BE BETTER TO DO THIS????
    if interval_param_ == "monthly_hist":
        date_length = 7
        hist_days = int(datetime.datetime.utcnow().timestamp()) / 86400 - start_hist_download_ux_timestamp / 86400 # for monthly_files
    elif interval_param_ == "daily_hist":
        date_length = 10
        hist_days = 35 # for all daily files
    elif interval_param_ == "monthly_update":
        date_length = 7
        hist_days = 1
    elif interval_param_ == "daily_update":
        date_length = 10
        hist_days = 3
    else:
        date_length = 10

    start_date = datetime.datetime.strptime(str(datetime.datetime.utcnow() - timedelta(days=hist_days))[0:10], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(str(datetime.datetime.utcnow() - timedelta(days=1))[0:10], "%Y-%m-%d") # 2021/10/05 changed 0 to 1
    delta = end_date - start_date
    l = []
    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
        l.insert(i, "" + market +"-"+ tick_interval +"-"+ str(day)[0:date_length] +"")
        # print(day)
    return sorted(list(set(l))) # works like distinct


def get_files_monthly():
    # todo: file import
    r = requests.get(base_url)
    open(file_path + ".zip", "wb").write(r.content)

    # todo: zip unpack
    with zipfile.ZipFile(file_path + ".zip", "r") as zip_ref:
        zip_ref.extractall(TMP_PATH[0:len(TMP_PATH)-1])

    # get data from csv file
    with open(file_path + ".csv") as file_handle:
        csv_reader = csv.reader(file_handle)
        csv_data = [row for row in csv_reader]

    open_time_min = min(csv_data)[0]
    open_time_max = max(csv_data)[0]

    # delete old data to overwrite
    cursor.execute("DELETE FROM " + db_schema_name + "." + db_table_name + " where open_time >= %s and open_time <= %s and tick_interval = %s and data_granulation = %s and market = %s and stock_type = %s and stock_exchange = %s and download_settings_id = %s", (open_time_min, open_time_max, tick_interval, data_granulation, market, stock_type, stock_exchange, download_settings_id))
    print("delete done")

    # insert data
    for i in csv_data:
        cursor.execute("INSERT INTO " + db_schema_name+"."+db_table_name +"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, `ignore`, market, tick_interval, data_granulation, stock_type, stock_exchange, download_settings_id, insert_ux_timestamp) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], market, tick_interval, data_granulation, stock_type, stock_exchange, download_settings_id, str(int(datetime.datetime.utcnow().timestamp()))))
        print(i)
    print("insert done")

    # update settings
    try:
        cursor.execute("UPDATE " + db_schema_name + "." + db_settings_table_name + " SET start_hist_download_ux_timestamp = %s, download_setting_status_id = %s where download_settings_id = %s", (str(int(str(open_time_max))/1000),  0, download_settings_id))
        print("update done")
    except Exception as e:
        print(e)
        cnxn.rollback()
        exit()


if __name__ == "__main__":
    delete_old_files()
    db_schema_name, db_table_name, db_settings_table_name = db_tables()
    cursor, cnxn = db_connect()

    """
    if first run: firstly get monthly files, secondly get daily files
    if monthly completed and daily not completed: get daily only
    
    else monthly completed and daily not completed: get daily only
    """
    # monthly
    download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, range_to_download, download_api_interval_sec, daily_update_from_files, monthly_update_from_files, start_hist_download_ux_timestamp = queue_works.get_settings(
        "monthly_hist")
    for k in get_filenames_to_download("monthly_hist"):
        try:
             file_path = TMP_PATH + k
             base_url = "https://data.binance.vision/data/"+stock_type+"/monthly/"+data_granulation+"/"+market+"/"+tick_interval+"/"+k+".zip"
             get_files_monthly()



             cnxn.commit()
        except Exception as e:
            print(e)
    # monthly_hist_complete = 1
    try:
        cursor.execute("UPDATE " + db_schema_name + "." + db_settings_table_name + " SET monthly_hist_complete = %s where download_settings_id = %s", (1, download_settings_id))
        print("update monthly hist complete done")
        cnxn.commit()
    except Exception as e:
        print(e)

    # daily
    delete_old_files()
    download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, range_to_download, download_api_interval_sec, daily_update_from_files, monthly_update_from_files, start_hist_download_ux_timestamp = queue_works.get_settings(
        "daily_hist")
    for k in get_filenames_to_download("daily_hist"):
        try:
             file_path = TMP_PATH + k
             base_url = "https://data.binance.vision/data/"+stock_type+"/daily/"+data_granulation+"/"+market+"/"+tick_interval+"/"+k+".zip"
             get_files_monthly()
             cnxn.commit()
        except Exception as e:
            print(e)
    try:
        cursor.execute("UPDATE " + db_schema_name + "." + db_settings_table_name + " SET daily_hist_complete = %s where download_settings_id = %s", (1, download_settings_id))
        print("update daily hist complete done")
        cnxn.commit()
    except Exception as e:
        print(e)

    cnxn.commit()
    cursor.close()
    cnxn.close()

    #  print(get_filenames_to_download("daily_hist")  # !!!!!!!!!!!!!!!!!!!!!! WHEN YOU ADD DAILY FILES, YOU CAN ERASE MONTHLY. MAYBE FIRST GET DAILY? OR MAYBE START FROM start_hist_download_ux_timestamp
    # or first get one more time settings. BUT YOU CAN CHOOSE WHAT COMBINATION WILL YOU GOT
    # but you can choose priority!!!!!.
    # remember that record can be blocked