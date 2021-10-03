# libs
import requests
import mysql.connector  # https://dev.mysql.com/doc/connector-python/en/
import json
import datetime



def get_conn_settings_from_json():
    # get database connection credentials from JSON file
    with open('db_credentials.json') as json_conf:
        sql_db_conn_ = (json.load(json_conf))
    return sql_db_conn_

sql_db_conn = get_conn_settings_from_json()




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


# todo: get this values from db or JSON. Make function
# settings. In the nearest future, get settings from json file or DB
# todo: Make function


cursor = cnxn.cursor()
cursor.execute("SELECT download_settings_id, market, tick_interval, stock_type, stock_exchange, current_range_to_overwrite, download_api_interval_sec FROM " + db_schema_name + "." + db_settings_table_name + " WHERE coalesce(next_download_ux_timestamp, 0) <= " + str(int(datetime.datetime.utcnow().timestamp())) + " order by next_download_ux_timestamp asc limit 1")
download_setting = cursor.fetchall()
download_settings_id = download_setting[0][0]
market = download_setting[0][1]
tick_interval = download_setting[0][2]
stock_type = download_setting[0][3]
stock_exchange = download_setting[0][4]
range_to_download = download_setting[0][5]
download_api_interval_sec = download_setting[0][6]



# todo: get "klines" from db

def get_binance_current_data():
    url = 'https://api.binance.com/api/v3/klines?symbol=' + market + '&interval=' + tick_interval
    data = requests.get(url).json()
    return data[-range_to_download:]

# todo: params 1,1,1 (get them from db)
# insert and overwrite fresh data
def fn_insert_overwrite_last_data():
    short_data = get_binance_current_data()
    try:
        cursor.execute("DELETE FROM " + db_schema_name+"."+db_table_name +" where open_time >= %s and tick_interval = %s and market = %s and stock_type = %s and stock_exchange = %s", (short_data[0][0], market, tick_interval, stock_type, stock_exchange))
        print("delete done")
        for i in short_data:
            cursor.execute("INSERT INTO " + db_schema_name+"."+db_table_name +"(open_time, open, high, low, close, volume, close_time, quote_asset_volume, number_of_trades, taker_buy_base_asset_volume, taker_buy_quote_asset_volume, `ignore`, market, tick_interval, stock_type, stock_exchange) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], market, tick_interval, stock_type, stock_exchange))
        print("insert done")
    except:
        print("error_1")

def fn_updatesettings_queue():
    try:
        cursor.execute("UPDATE " + db_schema_name + "." + db_settings_table_name + " SET last_download_ux_timestamp = %s, next_download_ux_timestamp = %s where download_settings_id = %s", (str(int(datetime.datetime.utcnow().timestamp())), str(int(str(int(datetime.datetime.utcnow().timestamp()))) + download_api_interval_sec), download_settings_id))
        print("update done")
        cnxn.commit()
        cursor.close()
        cnxn.close()
    except:
        print("error_2")

# todo: make code clear
def fn_get_binance_data():
    fn_insert_overwrite_last_data()
    fn_updatesettings_queue()

fn_get_binance_data()
