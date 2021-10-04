# libs
import requests
import datetime
from db_works import db_connect, db_tables

# get settings to download
def get_settings_current():
    db_schema_name, db_table_name, db_settings_table_name = db_tables()
    cursor, cnxn = db_connect()
    cursor.execute("SELECT download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, current_range_to_overwrite, download_api_interval_sec, daily_update_from_files, monthly_update_from_files FROM " + db_schema_name + "." + db_settings_table_name + " WHERE coalesce(next_download_ux_timestamp, 0) <= " + str(int(datetime.datetime.utcnow().timestamp())) + " order by next_download_ux_timestamp asc limit 1")
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
         print("no records")
         exit()


    # block current setting changing its status
    cursor.execute("UPDATE " + db_schema_name + "." + db_settings_table_name + " SET download_setting_status_id = %s where download_settings_id = %s", (1, download_settings_id))
    cnxn.commit()
    print("settings blocked")
    return download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, range_to_download, download_api_interval_sec, daily_update_from_files, monthly_update_from_files


# get data from binance API
def get_binance_data_current():
    url = "https://api.binance.com/api/v3/" + data_granulation + "?symbol=" + market + "&interval=" + tick_interval
    data = requests.get(url).json()
    return data[-range_to_download:]


# insert and overwrite fresh data
def insert_overwrite_data_current():
    db_schema_name, db_table_name, db_settings_table_name = db_tables()
    cursor, cnxn = db_connect()
    short_data = get_binance_data_current()
    try:
        cursor.execute("DELETE FROM " + db_schema_name+"."+db_table_name +" where open_time >= %s and market = %s and tick_interval = %s and data_granulation = %s  and stock_type = %s and stock_exchange = %s", (short_data[0][0], market, tick_interval, data_granulation, stock_type, stock_exchange))
        print("delete done")
        for i in short_data:
            cursor.execute("INSERT INTO " + db_schema_name+"."+db_table_name +"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, `ignore`, market, tick_interval, data_granulation, stock_type, stock_exchange, insert_ux_timestamp) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], market, tick_interval, data_granulation, stock_type, stock_exchange, str(int(datetime.datetime.utcnow().timestamp()))))
        print("insert done")
        cnxn.commit()
    except:
        print("error_1")


def update_settings_queue():
    db_schema_name, db_table_name, db_settings_table_name = db_tables()
    cursor, cnxn = db_connect()
    try:
        cursor.execute("UPDATE " + db_schema_name + "." + db_settings_table_name + " SET last_download_ux_timestamp = %s, next_download_ux_timestamp = %s, download_setting_status_id = %s where download_settings_id = %s", (str(int(datetime.datetime.utcnow().timestamp())), str(int(str(int(datetime.datetime.utcnow().timestamp()))) + download_api_interval_sec), 0, download_settings_id))
        print("update done")
        cnxn.commit()
        cursor.close()
        cnxn.close()
    except:
        print("error_2")


if __name__ == "__main__":
    download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, range_to_download, download_api_interval_sec, daily_update_from_files, monthly_update_from_files = get_settings_current()
    insert_overwrite_data_current()
    update_settings_queue()
