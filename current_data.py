# todo: DONE: work with monthly interwal - 1mo < works with files or 1M < works with API.
# todo: check commits and rollbacks

# libs
import requests
import datetime
from db_works import db_connect, db_tables
import stock_dwh_functions



# get data from binance API
def get_binance_data_current():
    url = "https://api.binance.com/api/v3/" + data_granulation + "?symbol=" + market + "&interval=" + (tick_interval).replace('1mo', '1M')
    data = requests.get(url).json()
    return data[-range_to_download:]


# insert and overwrite fresh data
def insert_overwrite_data_current():
    short_data = get_binance_data_current()
    try:
        cursor.execute("DELETE FROM " + db_schema_name+"."+db_table_name +" where open_time >= %s and market = %s and tick_interval = %s and data_granulation = %s  "
                                                                          "and stock_type = %s and stock_exchange = %s and download_settings_id = %s", (short_data[0][0], market, tick_interval, data_granulation, stock_type, stock_exchange, download_settings_id))
        print("delete done")
        for i in short_data:
            cursor.execute("INSERT INTO " + db_schema_name+"."+db_table_name +"(open_time, open, high, low, close, volume, close_time,"
                                                                              " quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, "
                                                                              "taker_buy_quote_asset_volume, `ignore`, market, tick_interval, data_granulation,"
                                                                              " stock_type, stock_exchange, download_settings_id, insert_ux_timestamp) "
                                                                              "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11],
                            market, tick_interval, data_granulation, stock_type, stock_exchange, download_settings_id,
                            str(int(datetime.datetime.utcnow().timestamp()))))
        print("insert done")
        cnxn.commit()
    except:
        print("error_1")
        cnxn.rollback()
        exit()



def update_settings_queue_current():
    try:
        cursor.execute("UPDATE " + db_schema_name + "." + db_settings_table_name + " SET last_download_ux_timestamp = %s, next_download_ux_timestamp = %s,"
                                                                                   " download_setting_status_id = %s where download_settings_id = %s",
                       (str(int(datetime.datetime.utcnow().timestamp())),
                        str(int(str(int(datetime.datetime.utcnow().timestamp()))) + download_api_interval_sec),
                        0, download_settings_id))
        print("update done")
    except:
        print("error_2")
        cnxn.rollback()
        exit()


if __name__ == "__main__":
    db_schema_name, db_table_name, db_settings_table_name = db_tables()
    cursor, cnxn = db_connect()
    download_settings_id, market, tick_interval, data_granulation, stock_type, stock_exchange, range_to_download, download_api_interval_sec, daily_update_from_files, monthly_update_from_files, start_hist_download_ux_timestamp = stock_dwh_functions.get_settings("current")
    insert_overwrite_data_current()
    update_settings_queue_current()
    # close connection
    cnxn.commit()
    cursor.close()
    cnxn.close()
